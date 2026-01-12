
import runpod
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path='backend/.env')
key = os.getenv('RUNPOD_API_KEY')
runpod.api_key = key

def force_update_minimal():
    endpoint_id = os.getenv('RUNPOD_ENDPOINT_ID')
    print(f"Forcing MINIMAL update on: {endpoint_id}")
    print(f"Key loaded: {key[:5]}...{key[-5:] if key else 'None'}")
    
    query = """
    mutation SaveEndpoint($input: EndpointInput!) {
        saveEndpoint(input: $input) {
            id
            env {
                key
                value
            }
        }
    }
    """
    
    variables = {
        "input": {
            "id": endpoint_id,
            "env": [
                {"key": "FORCE_RESTART", "value": str(datetime.now())}
            ]
        }
    }
    
    try:
        result = runpod.api.graphql.run_graphql_query(query, variables)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    force_update_minimal()
