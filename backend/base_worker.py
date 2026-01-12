import asyncio
import os
import socket
import time
import traceback
import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from pocketbase import PocketBase
from dotenv import load_dotenv

load_dotenv()

class BaseWorker(ABC):
    def __init__(self, 
                 task_types: List[str], 
                 max_concurrent_tasks: int = 5, 
                 poll_interval: int = 5):
        self.worker_id = f"worker-{socket.gethostname()}-{os.getpid()}"
        self.task_types = task_types
        self.max_concurrent_tasks = max_concurrent_tasks
        self.poll_interval = poll_interval
        self.running = False
        
        # Init PocketBase
        self.pb_url = os.getenv("PB_URL", "https://uncensored-engine-db.fly.dev") 
        self.pb = PocketBase(self.pb_url)
        
        # Authenticate as Admin (needed to process jobs)
        self.admin_email = os.getenv("PB_ADMIN_EMAIL", "admin@example.com")
        self.admin_pass = os.getenv("PB_ADMIN_PASS", "password123456")

        print(f"🤖 Worker initialized: {self.worker_id}")
        print(f"   Task types: {', '.join(self.task_types)}")
        print(f"   DB: {self.pb_url}")

    async def _authenticate(self):
        try:
            # Use direct HTTP request to avoid SDK issues
            auth_url = f"{self.pb_url}/api/admins/auth-with-password"
            response = requests.post(auth_url, json={
                "identity": self.admin_email,
                "password": self.admin_pass
            })
            response.raise_for_status()
            auth_data = response.json()

            # Set the auth token manually
            self.pb.auth_store.save(auth_data.get('token'), auth_data.get('admin'))
            print("✅ PocketBase Admin Auth Success")
        except Exception as e:
            print(f"⚠️ Auth failed: {e}")

    async def start(self):
        """
        Start the worker polling loop.
        """
        self.running = True
        print(f"▶️  Worker started: {self.worker_id}")
        await self._authenticate()

        while self.running:
            try:
                # Claim tasks
                tasks = await self.claim_tasks()

                if not tasks:
                    await asyncio.sleep(self.poll_interval)
                    continue

                print(f"📋 Claimed {len(tasks)} task(s)")

                # Process tasks concurrently
                await asyncio.gather(*[self.process_safe_task(task) for task in tasks])

            except Exception as e:
                print(f"❌ Worker loop error: {e}")
                await asyncio.sleep(10)

    def stop(self):
        """
        Stop the worker.
        """
        print(f"⏸  Stopping worker: {self.worker_id}")
        self.running = False

    async def claim_tasks(self) -> List[Dict]:
        """
        Poll for 'queued' jobs in PocketBase.
        """
        try:
            # PocketBase filter syntax
            filter_parts = [f"type='{t}'" for t in self.task_types]
            type_filter = f"({' || '.join(filter_parts)})"
            filter_str = f"status='queued' && {type_filter}"

            records = self.pb.collection('jobs').get_list(
                page=1,
                per_page=5, 
                query_params={
                    "filter": filter_str,
                    "sort": "+created"
                }
            )
            
            if not records.items:
                return []

            task_record = records.items[0]
            
            # Claim it
            self.pb.collection('jobs').update(task_record.id, {
                "status": "processing",
                "worker_id": self.worker_id,
                "started_at": datetime.utcnow().isoformat()
            })
            
            # Return as dict
            task_dict = {
                'id': task_record.id,
                'type': task_record.type,
                'params': task_record.params,
                'input': task_record.params, 
                'status': 'processing',
                'user_id': task_record.user_id
            }
            return [task_dict]
            
        except Exception as e:
            print(f"⚠️ Error claiming tasks: {e}")
            traceback.print_exc()
            return []

    async def process_safe_task(self, task: Dict):
        """
        Wrapper to process a task with error handling.
        """
        task_id = task.get('id')
        
        try:
            # Execute the abstract process method
            result = await self.process_task(task)

            # status update
            success = result.get('success', False)
            
            update_data = {
                "status": "completed" if success else "failed",
                "result": result, 
                "completed_at": datetime.utcnow().isoformat()
            }
            
            if not success and 'error' in result:
                update_data["error"] = result['error']
            
            self.pb.collection('jobs').update(task_id, update_data)
            print(f"✅ Task {task_id} finished")

        except Exception as e:
            print(f"🔥 Task failed: {e}")
            traceback.print_exc()
            try:
                self.pb.collection('jobs').update(task_id, {
                    "status": "failed",
                    "error": str(e)
                })
            except:
                pass

    @abstractmethod
    async def process_task(self, task: Dict) -> Dict:
        """
        Implement specific task processing logic.
        """
        pass
