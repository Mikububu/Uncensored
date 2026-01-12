
import requests
import json

def explore_myself():
    api_key = "os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")"
    url = "https://api.runpod.io/graphql"
    
    # Introspection query for 'myself' type
    query = """
    query {
      __type(name: "User") {
        fields {
          name
          type {
            name
            kind
          }
        }
      }
    }
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json={"query": query}, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    explore_myself()
