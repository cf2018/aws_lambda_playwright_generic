# Playwright Flask Generic Tool

A Flask application that provides a generic API for executing Playwright code remotely. This tool allows you to send Python code that uses Playwright to perform web automation tasks like scraping, testing, screenshots, and form interactions.

## Features

- **Generic Code Execution**: Send any Playwright Python code to be executed remotely
- **Web Interface**: User-friendly web form for testing and executing code
- **Browser Management**: Configurable browser and context options
- **Error Handling**: Comprehensive error reporting with stack traces
- **Examples**: Built-in examples for common use cases
- **RESTful API**: Simple HTTP endpoints for integration
- **Client Library**: Python client for easy integration

## Setup

1. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Start the Flask application**:
   ```bash
   python app.py
   ```

   Or use the convenient startup script:
   ```bash
   ./start_web.sh
   ```

The application will be available at `http://localhost:5001`

### Web Interface

Visit `http://localhost:5001/web` for a user-friendly web interface that includes:

- **Code Editor**: Syntax-highlighted textarea for writing Playwright code
- **Browser Options**: Checkboxes for headless mode, slow motion, etc.
- **Viewport Settings**: Configurable window size
- **Quick Examples**: Pre-built examples you can load with one click
- **Real-time Results**: Formatted JSON output with success/error states
- **Responsive Design**: Works on desktop and mobile devices

## API Endpoints

### GET /
Returns API documentation and available endpoints.

### POST /execute
Execute Playwright code.

**Request Body**:
```json
{
    "code": "await page.goto('https://example.com')\nresult = await page.title()",
    "browser_options": {
        "headless": true,
        "args": ["--no-sandbox"]
    },
    "context_options": {
        "viewport": {"width": 1920, "height": 1080}
    }
}
```

**Response**:
```json
{
    "success": true,
    "result": "Example Domain",
    "error": null,
    "metadata": {
        "url": "https://example.com",
        "title": "Example Domain",
        "viewport": {"width": 1920, "height": 1080}
    }
}
```

### GET /examples
Returns example code snippets for common use cases.

### GET /health
Health check endpoint.

## Usage Examples

### 1. Using the Web Interface (Recommended for Testing)

1. Start the Flask app: `./start_web.sh`
2. Open your browser to `http://localhost:5001/web`
3. Try the pre-loaded example or click on "Quick Examples"
4. Modify the code as needed and click "Execute Code"
5. View the results in real-time

### 2. Using the API directly with curl

```bash
# Simple navigation
curl -X POST http://localhost:5001/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "await page.goto('\''https://example.com'\'')\ntitle = await page.title()\nresult = {'\''title'\'': title, '\''url'\'': page.url}"
  }'

# Take screenshot
curl -X POST http://localhost:5001/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "await page.goto('\''https://example.com'\'')\nscreenshot = await page.screenshot()\nresult = {'\''screenshot_size'\'': len(screenshot)}"
  }'
```

### 3. Using the Python client

```python
from client_example import PlaywrightClient

client = PlaywrightClient("http://localhost:5001")

# Simple navigation
result = client.execute("""
await page.goto('https://example.com')
title = await page.title()
result = {'title': title, 'url': page.url}
""")

print(result)
```

### 4. Web scraping example

```python
scraping_code = """
await page.goto('https://quotes.toscrape.com/')
quotes = await page.locator('.quote').all()
result = []
for quote in quotes[:3]:
    text = await quote.locator('.text').inner_text()
    author = await quote.locator('.author').inner_text()
    result.append({'text': text, 'author': author})
"""

result = client.execute(scraping_code)
```

### 5. Form interaction example

```python
form_code = """
await page.goto('https://httpbin.org/forms/post')
await page.fill('input[name="custname"]', 'John Doe')
await page.fill('input[name="custtel"]', '1234567890')
await page.fill('input[name="custemail"]', 'john@example.com')
await page.click('input[type="submit"]')
await page.wait_for_load_state('networkidle')
result = {'final_url': page.url, 'success': True}
"""

result = client.execute(form_code)
```

## Available Variables in Code

When executing code, you have access to these variables:

- `page`: The Playwright page object
- `context`: The browser context object
- `browser`: The browser object
- `p`: The Playwright object
- `asyncio`: The asyncio module
- `json`: The json module

## Browser Configuration

You can customize browser behavior using `browser_options` and `context_options`:

```python
browser_options = {
    "headless": False,  # Run in visible mode
    "args": ["--start-maximized"],
    "slow_mo": 1000  # Slow down operations
}

context_options = {
    "viewport": {"width": 1366, "height": 768},
    "user_agent": "Custom User Agent",
    "locale": "en-US"
}

result = client.execute(code, browser_options, context_options)
```

## Error Handling

The API provides detailed error information:

```json
{
    "success": false,
    "result": null,
    "error": {
        "message": "Error description",
        "type": "ErrorType",
        "traceback": "Full stack trace"
    }
}
```

## Security Notes

- This tool executes arbitrary Python code, so use it in a controlled environment
- Consider implementing authentication for production use
- The browser runs with `--no-sandbox` flag for compatibility

## Dependencies

- Flask 3.0.0
- Playwright 1.40.0
- python-dotenv 1.0.0

## License

This project is open source and available under the MIT License.
