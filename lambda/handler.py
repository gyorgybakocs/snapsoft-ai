import json

def handler(event, context):
    print("STARTING PROCESS")
    print(json.dumps(event))

    return {
        "statusCode": 200,
        "body": "ok"
    }
