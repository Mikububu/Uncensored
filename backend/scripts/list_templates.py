
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path='backend/.env')
api_key = os.getenv("RUNPOD_API_KEY")

def list_templates():
    url = "https://api.runpod.io/graphql"
    
    # Query for public templates is difficult purely via API without knowing the structure
    # But we can list "my" templates.
    # To find public ones, we might need to search or use a known public ID.
    # "runpod/stable-diffusion:v1-5" is a standard image.
    
    query = """
    query {
      myself {
        podTemplates {
          id
          name
          imageName
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
        data = r.json()
        print(json.dumps(data, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_templates()
