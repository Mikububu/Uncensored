
import os
import requests
import json
import argparse

def get_template_details():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template_id", default="7512t5qg4h")
    args = parser.parse_args()

    api_key = "os.getenv("RUNPOD_API_KEY") or os.getenv("RUNPOD_KEY")"
    url = "https://api.runpod.io/graphql"
    
    query = f"""
    query {{
      template(id: "{args.template_id}") {{
        id
        name
        imageName
        dockerArgs
        containerDiskInGb
        env {{
          key
          value
        }}
        isPublic
      }}
    }}
    """
    # Note: 'template(id: ...)' is the correct query for public/specific templates
    # The previous script queried 'myself { templates }' which only lists user's templates.

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(url, headers=headers, json={"query": query})
        r.raise_for_status()
        data = r.json()
        print(json.dumps(data, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_template_details()
