import runpod
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("RUNPOD_API_KEY")
endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID_SDXL")

runpod.api_key = api_key

if not endpoint_id:
    print("No endpoint ID found")
    exit(1)

print(f"Inspecting endpoint: {endpoint_id}")
endpoint = runpod.Endpoint(endpoint_id)

try:
    # Run a dummy job
    job = endpoint.run({"input": {"prompt": "test"}})
    print("Job Object Type:", type(job))
    print("Job Object Dir:", dir(job))
    print("Job Object Dict:", job.__dict__ if hasattr(job, '__dict__') else "No dict")
except Exception as e:
    print(f"Error: {e}")
