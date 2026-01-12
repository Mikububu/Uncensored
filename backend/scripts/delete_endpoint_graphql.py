
import os
import requests
import argparse
from dotenv import load_dotenv

load_dotenv()

def delete_endpoint():
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint_id", required=True)
    args = parser.parse_args()

    api_key = os.getenv("RUNPOD_API_KEY", "os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")")
    url = "https://api.runpod.io/graphql"

    query = f"""
    mutation {{
        deleteEndpoint(id: "{args.endpoint_id}")
    }}
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(url, json={"query": query}, headers=headers)
        print(f"Delete Result: {r.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    delete_endpoint()
