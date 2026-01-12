import asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from z_image_worker import ZImageWorker

# Global worker instance
worker = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Life span events: Start worker on startup, stop on shutdown.
    Fly.io will run this server, which in turn runs the worker loop.
    """
    global worker
    # Check if we are in a worker role or if we just want to run it alongside api
    # For simple deployments, running it alongside is fine.
    try:
        worker = ZImageWorker()
        # Run worker in background task
        task = asyncio.create_task(worker.start())
        print("🚀 Background worker started")
    except Exception as e:
        print(f"⚠️ Failed to start worker: {e}")
    
    yield
    
    if worker:
        worker.stop()
        print("🛑 Background worker stopped")

app = FastAPI(title="Z-Image-Turbo Backend", lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "ok", "service": "z-image-turbo-worker"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/admin/metrics")
async def admin_metrics():
    """Proxy endpoint to get metrics from the worker logic"""
    if not worker:
        return {"error": "Worker not initialized"}
    return await worker.get_admin_metrics()

