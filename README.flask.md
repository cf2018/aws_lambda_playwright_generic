# Playwright Flask Generic Tool (Flask Version)

This README is for running the project as a standard Flask web application (local development or traditional server deployment).

## Features
- Web UI and REST API for executing Playwright Python code
- Quick examples, cURL generator, and real-time results

## Quickstart

1. **Build the Docker image:**
   ```bash
   docker build -f Dockerfile.flask -t playwright-flask .
   ```
2. **Run the container:**
   ```bash
   docker run -p 5001:5001 playwright-flask
   ```
3. **Access the web UI:**
   Open [http://localhost:5001/web](http://localhost:5001/web)

## API Usage
- POST to `http://localhost:5001/execute` with the same JSON payload as described in the main README.

## Development
- You can also run locally with Python:
  ```bash
  pip install -r requirements.txt
  playwright install --with-deps
  python app.py
  ```

## Notes
- This mode is best for local development, testing, and non-serverless deployments.
