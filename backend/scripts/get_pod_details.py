
import runpod
import os
from dotenv import load_dotenv
import json

load_dotenv(dotenv_path='backend/.env')
runpod.api_key = os.getenv('RUNPOD_API_KEY')

def get_pod_details():
    try:
        # The library might expose this differently. 
        # Checking if we can get all pods.
        # runpod-python's API surface is sometimes tricky.
        # Often it uses GraphQL under the hood.
        

        # Check specific pod
        query = """
        query GetPod {
            pod(input: {podId: "24hz46kbtb2si8"}) {
                id
                desiredStatus
                lastStatusChange
                runtime {
                    gpus {
                        id
                    }
                    container {
                        imageName
                        status
                    }
                }
            }
        }
        """
        result = runpod.api.graphql.run_graphql_query(query)
        print(f"Result: {result}")

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    get_pod_details()
