# Playwright Flask Generic Tool (AWS Lambda Version)

This README is for deploying and running the project as an AWS Lambda function (container image).

## Features
- Compatible with AWS Lambda and API Gateway
- Same API and code execution as Flask version

## Quickstart (Local Lambda Testing)

1. **Build the Lambda Docker image:**
   ```bash
   docker build -f Dockerfile.lambda -t playwright-lambda .
   ```
2. **Run the Lambda container locally:**
   ```bash
   docker run -p 9000:8080 playwright-lambda
   ```
3. **Invoke the Lambda function locally:**
   ```bash
   curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
     -d '{"body": "{ ...your JSON payload... }"}'
   ```
   - The payload should be a stringified JSON object in the `body` field (as required by Lambda proxy integration).

## Deploying to AWS Lambda
- Push the image to ECR and create a Lambda function from the container image.
- Set the handler to `app.lambda_handler`.
- Use API Gateway to expose an HTTP endpoint if needed.

## Notes
- This mode is best for serverless, scalable deployments on AWS.
- The Lambda handler wraps the Flask app using a WSGI adapter (see `app.py`).
