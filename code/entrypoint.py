# Copyright (c) 2019 Lightricks. All rights reserved.

import json

ASIAN_COUNTRIES = {"CN", "JP"}

def handler(event, context):
    print(json.dumps(event))

    query_parameters = event.get("queryStringParameters") or {}
    country = query_parameters.get("country", "N/A")

    products = ["Yearly1", "Monthly1", "OTP1"]

    if country in ASIAN_COUNTRIES:
        products = ["Yearly2", "Monthly2", "OTP2"]

    body = {
        "products": products
    }

    return {
        "body": json.dumps(body),
        "headers": {
            "content-type": "application/json"
        }
    }
