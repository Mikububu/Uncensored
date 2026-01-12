
import requests
import json

def get_runpod_balance():
    api_key = "os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")"
    url = "https://api.runpod.io/graphql"
    
    # query { myself { balance } } is common, but let's try to get everything under myself
    query = """
    query {
      myself {
        id
        clientBalance
      }
    }
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print(f"Sending request to {url}")
    print(f"Headers: {headers}")
    print(f"Query: {query}")

    try:
        response = requests.post(url, json={"query": query}, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Raw Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if 'errors' in data:
                print("GraphQL Errors found.")
                # Maybe balance is directly under myself
                query_alt = "query { myself { balance } }"
                print(f"Trying alternative query: {query_alt}")
                response = requests.post(url, json={"query": query_alt}, headers=headers)
                print(f"Alt Raw Response: {response.text}")
            else:
                print("Success!")
        else:
            print("Request failed.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_runpod_balance()
