# Copyright (c) 2019 Lightricks. All rights reserved.

import json

def handler(event, context):
    print(json.dumps(event))
    print(context)

    query_parameters = event.get("queryStringParameters") or {}
    name = query_parameters.get("name", "N/A")

    return {
        "body": "Hi %s! Welcome to the cloud" % name,
    }
