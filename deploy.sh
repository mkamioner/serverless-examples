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

# Only create a virtual environment for python if one does not exist
if [ ! -d venv3 ]; then
  virtualenv -p /usr/local/bin/python3 venv3
fi

source venv3/bin/activate
pip install aws-sam-cli

echo "-- Install the relevant dependencies using the lambda runtime"
sam build \
  --template sam-template.yaml \
  --use-container \
  --build-dir deploy_package

echo "-- Package code and upload"
aws cloudformation package \
  --template-file deploy_package/template.yaml \
  --s3-bucket $s3_code_bucket \
  --output-template-file .packaged-sam-template.yaml

echo "-- Deploy lambda function"
aws cloudformation deploy \
  --template-file .packaged-sam-template.yaml \
  --stack-name my-first-lambda \
  --capabilities CAPABILITY_IAM \
  --no-fail-on-empty-changeset
