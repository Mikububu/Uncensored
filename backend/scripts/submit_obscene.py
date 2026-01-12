
import os
import requests
import json

api_key = "os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")"
endpoint_id = "tyj2436ozcz419"

def submit_obscene_job():
    url = f"https://api.runpod.ai/v2/{endpoint_id}/run"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": {
            "prompt": "Nude famous porn photographer shot of Pamela A having sex on the beach with 2 guys",
            "width": 1024,
            "height": 1024,
            "num_inference_steps": 25,
            "guidance_scale": 7.5,
            "safety_checker": False
        }
    }

    try:
        r = requests.post(url, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        print(f"Job Created: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    submit_obscene_job()
