
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path='backend/.env')
api_key = os.getenv('RUNPOD_API_KEY')
template_id = "5ugs7iop50"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def get_template_details():
    url = "https://api.runpod.io/graphql"
    
    query = """
    query Template($id: String!) {
      podTemplate(id: $id) {
        id
        name
        imageName
        dockerArgs
        containerDiskInGb
        volumeInGb
        volumeMountPath
        env {
            key
            value
        }
      }
    }
    """
    
    try:
        r = requests.post(url, headers=headers, json={"query": query, "variables": {"id": template_id}})
        r.raise_for_status()
        data = r.json()
        t = data.get('data', {}).get('podTemplate')
        
        if t:
            print(f"Template: {t['name']} ({t['id']})")
            print(f"Image: {t['imageName']}")
            print(f"Env: {json.dumps(t.get('env'), indent=2)}")
            return t
        
        print("Template not found.")
        print(f"Raw Response: {json.dumps(data, indent=2)}")
             
    except Exception as e:
        print(f"Error: {e}")
             
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_template_details()
