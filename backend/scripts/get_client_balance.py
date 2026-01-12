
import requests
import json

def get_runpod_balance():
    api_key = "os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")"
    url = "https://api.runpod.io/graphql"
    
    query = """
    query {
      myself {
        clientBalance
      }
    }
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(url, json={"query": query}, headers=headers)
        data = r.json()
        balance = data.get('data', {}).get('myself', {}).get('clientBalance')
        print(f"Current RunPod Balance ($): {balance}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_runpod_balance()
