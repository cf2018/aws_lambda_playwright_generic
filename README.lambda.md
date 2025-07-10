# Playwright Flask Generic Tool (AWS Lambda Version)

This README is for deploying and running the project as an AWS Lambda function (container image).

## Features
- Compatible with AWS Lambda (no API Gateway required)
- Same code execution as Flask version

## Quickstart (Local Lambda Testing)

1. **Build the Lambda Docker image:**
   ```bash
   docker build -f Dockerfile.lambda -t playwright-lambda .
   ```
2. **Run the Lambda container locally:**
   ```bash
   docker run -p 9001:8080 playwright-lambda
   ```
3. **Invoke the Lambda function locally:**
   ```bash
   curl -XPOST "http://localhost:9001/2015-03-31/functions/function/invocations" \
     -H "Content-Type: application/json" \
     -d '{"code": "await page.goto(\\"https://www.w3schools.com/html/html_page_title.asp\\")\\ntitle = await page.title()\\nresult = {\\"title\\": title}\nreturn result"}'
   ```
   **Expected response:**
   ```json
   {
     "success": true,
     "result": {"title": "HTML Page Title"},
     "error": null,
     "metadata": {
       "url": "https://www.w3schools.com/html/html_page_title.asp",
       "viewport": {"width": 0, "height": 0}
     }
   }
   ```

4. **Deploy to AWS Lambda**
- Push the image to ECR and create a Lambda function from it.
- Set the handler to `app.lambda_handler`.
- Invoke directly with a JSON payload as above (no API Gateway needed).

## Notes
- This mode is best for serverless, scalable deployments on AWS.
- The Lambda handler is a plain Python function for direct invocation.

---

For more usage examples, see `client_example.py` and the main README.
