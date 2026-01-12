import os
import requests
import json
from dotenv import load_dotenv

load_dotenv('backend/.env')
api_key = os.getenv('RUNPOD_API_KEY')
endpoint_id = os.getenv('RUNPOD_ENDPOINT_ID')

def get_endpoint_workers():
    url = "https://api.runpod.io/graphql"
    
    query = """
    query {
      myself {
        serverlessDiscount {
          discountFactor
          type
          expirationDate
        }
      }
    }
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        r = requests.post(url, json={"query": query}, headers=headers)
        r.raise_for_status()
        data = r.json()
        print(f"Endpoint Workers: {json.dumps(data, indent=2)}")
        return data
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_endpoint_workers()
