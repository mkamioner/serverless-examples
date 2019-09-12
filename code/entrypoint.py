# Copyright (c) 2019 Lightricks. All rights reserved.

from io import BytesIO
import json

from PIL import Image
import boto3

S3_CLIENT = boto3.client("s3")
IMAGE_WIDTH_SIZES = [120, 240, 480]

def _extract_bucket_and_key_from_record(record):
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    return bucket, key

def _resize_picture(bucket, key, width_size):
    print("Resizing picture %s/%s to width of %s" % (bucket, key, width_size))
    file_name = key.split("/")[-1]

    # Load the image from S3
    original_data = S3_CLIENT.get_object(Bucket=bucket, Key=key)["Body"].read()

    # Resize the image
    img = Image.open(BytesIO(original_data))
    width_percent = float(width_size / float(img.size[0]))
    horizontal_size = int((float(img.size[1]) * width_percent))
    img = img.resize((width_size, horizontal_size), Image.ANTIALIAS)
    buffer = BytesIO()
    img.save(buffer, "JPEG")

    # Save the new resized image to the cloud
    new_key = "resized/%s_%s" % (width_size, file_name)
    buffer.seek(0)
    S3_CLIENT.put_object(Bucket=bucket, Key=new_key, Body=buffer)

def handler(event, context):
    print(json.dumps(event))

    for record in event.get("Records"):
        bucket, key = _extract_bucket_and_key_from_record(record)
        for width_size in IMAGE_WIDTH_SIZES:
            _resize_picture(bucket, key, width_size)
