#! /bin/bash

set -e

# We want to work with the Lightricks dev account, not production.
export AWS_PROFILE=dev

# Let's deploy to Ireland for this example. There are not a lot of existing resources there so it
# will be easier identify our changes.
export AWS_DEFAULT_REGION=eu-west-1

# This is where we upload the code for our function. It must exist before we upload and in the same
# region that the lambda function exists in.
s3_code_bucket="lightricks-staging-lambda-code-eu-west-1"

echo "-- Package code and upload"
aws cloudformation package \
  --template-file sam-template.yaml \
  --s3-bucket $s3_code_bucket \
  --output-template-file .packaged-sam-template.yaml

echo "-- Deploy lambda function"
aws cloudformation deploy \
  --template-file .packaged-sam-template.yaml \
  --stack-name my-first-lambda \
  --capabilities CAPABILITY_IAM \
  --no-fail-on-empty-changeset


url=$(
  aws cloudformation describe-stacks \
    --stack-name my-first-lambda \
    --output text \
    --query "Stacks[0].Outputs[?OutputKey=='Url'].OutputValue"
)

echo "-- Use the following URL to access your new API: ${url}"
