
import requests
import json

def try_all_balance_fields():
    api_key = "os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")"
    url = "https://api.runpod.io/graphql"
    
    # Try a broad query with common field names
    query = """
    query {
      myself {
        id
        email
      }
    }
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print("Checking if token is valid first...")
    try:
        r = requests.post(url, json={"query": query}, headers=headers)
        print(f"Token Check Status: {r.status_code}")
        print(f"Token Check Body: {r.text}")
        
        # Now try different balance fields one by one to isolate which one works
        fields_to_try = ["balance", "credits", "amount", "credit"]
        for field in fields_to_try:
            print(f"Trying field: {field}")
            q = "query { myself { " + field + " } }"
            rj = requests.post(url, json={"query": q}, headers=headers)
            print(f"Result for {field}: {rj.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try_all_balance_fields()
