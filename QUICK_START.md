# 🚀 Playwright Generic Tool - Quick Start Guide

## 📁 Project Structure

```
aws_lambda_playwright_generic/
├── app.py                 # Main Flask app & Lambda handler
├── templates/             # HTML templates (web UI)
│   └── index.html         # Web interface template
├── static/                # Static files (CSS, JS)
│   └── style.css          # Custom styling
├── client_example.py      # Python client with examples
├── demo.py                # Demo script to test functionality
├── start_web.sh           # Startup script for Flask
├── requirements.txt       # Python dependencies
├── setup.sh               # Setup script for installation
├── test_api.py            # API test suite
├── test_web_interface.py  # Web interface testing
├── test_flask_app.py      # Flask app testing
├── test_install.sh        # Installation verification
├── Dockerfile.flask       # Dockerfile for Flask app
├── Dockerfile.lambda      # Dockerfile for AWS Lambda
├── README.md              # Comprehensive documentation
├── README.flask.md        # Flask-specific docs
├── README.lambda.md       # Lambda-specific docs
├── QUICK_START.md         # This file
├── .gitignore             # Git ignore file
└── venv/                  # Virtual environment
```

## 🎯 What You've Built

A **generic Playwright automation tool** that can run as:
- **Flask app** (local/dev, with web UI and REST API)
- **AWS Lambda function** (serverless, direct invocation)

You can:
- **Web Scraping**
- **Screenshots**
- **Form Automation**
- **Testing**
- **Any Playwright Task**

---

## ⚡️ Quick Start: Flask (Local/Dev)

1. **Setup:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   source venv/bin/activate
   pip install -r requirements.txt
   playwright install --with-deps
   ```
2. **Run Flask app:**
   ```bash
   python app.py
   # or
   ./start_web.sh
   # or with Docker:
   docker build -f Dockerfile.flask -t playwright-flask .
   docker run -p 5001:5001 playwright-flask
   ```
3. **Access:**
   - Web UI: [http://localhost:5001/web](http://localhost:5001/web)
   - API: [http://localhost:5001/execute](http://localhost:5001/execute)

---

## ⚡️ Quick Start: AWS Lambda (Serverless)

1. **Build Lambda Docker image:**
   ```bash
   docker build -f Dockerfile.lambda -t playwright-lambda .
   ```
2. **Run Lambda container locally:**
   ```bash
   docker run -p 9001:8080 playwright-lambda
   ```
3. **Invoke Lambda locally:**
   ```bash
   curl -XPOST "http://localhost:9001/2015-03-31/functions/function/invocations" \
     -H "Content-Type: application/json" \
     -d '{"code": "await page.goto(\\"https://example.com\\")\\ntitle = await page.title()\\nresult = {\\"title\\": title, \\"url\\": page.url}\nreturn result"}'
   ```
   - The response will include your result and metadata.
4. **Deploy to AWS Lambda:**
   - Push the image to ECR and create a Lambda function from it.
   - Set the handler to `app.lambda_handler`.
   - Invoke directly with a JSON payload (no API Gateway needed).

---

## 🌐 Web Interface (Flask only)
- Code editor with syntax highlighting
- Browser configuration options
- Quick-load examples
- Real-time result display
- Mobile-responsive design

## 📋 API Endpoints (Flask only)
- `POST /execute` — Execute Playwright code
- `GET /examples` — Get code examples
- `GET /health` — Health check
- `GET /` — API documentation

## 🎮 Usage Examples
- See `client_example.py` for Python usage
- See `demo.py` for a demo script
- Use cURL as shown above for both Flask and Lambda

## 🧪 Testing
- `./test_install.sh` — Test installation
- `python demo.py` — Run demo
- `python test_api.py` — Test API (Flask)
- `python client_example.py` — Use client examples

## 📦 Available Variables in Code
- `page`, `context`, `browser`, `p`, `asyncio`, `json`

## ⚙️ Browser Configuration
- See `client_example.py` and docs for options

## 🛡️ Security Notes
- Executes arbitrary Python code — use in a controlled environment
- Consider authentication for production
- Browser runs with `--no-sandbox` for compatibility

## 🎉 You're Ready!

- For Flask: use the web UI or REST API.
- For Lambda: invoke with a JSON payload as shown above.
- See `README.flask.md` and `README.lambda.md` for more details on each mode.

Happy automating! 🎭🚀
