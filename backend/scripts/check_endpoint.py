
import runpod
import os
from dotenv import load_dotenv
import json

load_dotenv(dotenv_path='backend/.env')
runpod.api_key = os.getenv('RUNPOD_API_KEY')

def check_endpoint():
    try:
        # Query for Serverless Endpoints
        query = """
        query Mysore {
            myself {
                endpoints {
                    id
                    name
                    gpuIds
                    idleTimeout
                    templateId
                    workersMin
                    workersMax
                }
            }
        }
        """
        result = runpod.api.graphql.run_graphql_query(query)
        if 'errors' in result:
             print(f"Error: {result['errors']}")
             return

        endpoints = result['data']['myself']['endpoints']
        
        print("--- ALL ENDPOINTS ---")
        for ep in endpoints:
             print(f"ID: {ep['id']} | Name: {ep['name']} | MaxWorkers: {ep['workersMax']} | MinWorkers: {ep['workersMin']}")


    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    check_endpoint()
