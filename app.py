from flask import Flask, request, jsonify, render_template
import asyncio
import json
import traceback
from playwright.async_api import async_playwright
import inspect
import sys
from typing import Any, Dict

app = Flask(__name__)

class PlaywrightExecutor:
    """Generic Playwright code executor"""
    
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
    
    async def execute_code(self, code: str, browser_options: Dict = None, context_options: Dict = None) -> Dict[str, Any]:
        """
        Execute generic Playwright code
        
        Args:
            code: Python code string to execute (should use 'page' variable)
            browser_options: Options for browser launch
            context_options: Options for browser context
        
        Returns:
            Dict with result, error, and metadata
        """
        result = {
            "success": False,
            "result": None,
            "error": None,
            "metadata": {}
        }
        
        try:
            # Add timeout for the entire operation using asyncio.wait_for
            async def _execute_with_playwright():
                async with async_playwright() as p:
                    # Default browser options with better compatibility
                    # Launch browser with anti-bot options
                    default_browser_options = {
                        "headless": True,
                        "args": [
                            "--no-sandbox",
                            "--disable-dev-shm-usage",
                            "--disable-gpu",
                            "--disable-web-security",
                            "--disable-features=VizDisplayCompositor",
                            "--disable-blink-features=AutomationControlled",
                            "--disable-infobars"
                        ]
                    }
                    if browser_options:
                        default_browser_options.update(browser_options)
                    
                    # Launch browser
                    browser = await p.chromium.launch(**default_browser_options)
                    
                    # Create context with user agent and locale for anti-bot
                    default_context_options = {
                        "viewport": {"width": 1920, "height": 1080},
                        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "locale": "es-AR"
                    }
                    if context_options:
                        default_context_options.update(context_options)
                    
                    # Create context and page
                    context = await browser.new_context(**default_context_options)
                    page = await context.new_page()
                    
                    # Set default timeout for page operations
                    page.set_default_timeout(30000)  # 30 seconds
                    
                    # Prepare execution environment
                    execution_globals = {
                        "page": page,
                        "context": context,
                        "browser": browser,
                        "p": p,
                        "asyncio": asyncio,
                        "json": json
                    }
                    
                    # Execute the user code
                    exec_result = None
                    if code.strip():
                        indented_code = '\n'.join('    ' + line if line.strip() else '' for line in code.split('\n'))
                        wrapped_code = f"""
async def _user_function():
{indented_code}
"""
                        exec(wrapped_code, execution_globals)
                        user_func = execution_globals.get('_user_function')
                        if user_func:
                            exec_result = await user_func()
                        # Restore Playwright objects in globals in case user code overwrote them
                        execution_globals['page'] = page
                        execution_globals['context'] = context
                        execution_globals['browser'] = browser
                        # Remove any overwritten builtins or Playwright methods
                        for var in ['result', 'title', 'page', 'context', 'browser']:
                            if var in execution_globals and execution_globals[var] is not locals().get(var):
                                del execution_globals[var]
                    # Get page info for metadata (with error handling)
                    try:
                        # Always use the local page object, not from execution_globals
                        metadata = {
                            "url": page.url,
                           # "title": await page.title(),
                            "viewport": await page.viewport_size()
                        }
                    except Exception as meta_error:
                        metadata = {
                            "url": getattr(page, 'url', 'unknown'),
                           # "title": f"Error getting title: {str(meta_error)}",
                            "viewport": {"width": 0, "height": 0}
                        }
                    
                    await browser.close()
                    return exec_result, metadata
            
            # Execute with timeout
            exec_result, metadata = await asyncio.wait_for(_execute_with_playwright(), timeout=60.0)
            
            result["metadata"] = metadata
            result["success"] = True
            result["result"] = exec_result
                    
        except asyncio.TimeoutError:
            result["error"] = {
                "message": "Operation timed out after 60 seconds",
                "type": "TimeoutError",
                "traceback": "Operation exceeded maximum allowed time"
            }
        except Exception as e:
            result["error"] = {
                "message": str(e),
                "type": type(e).__name__,
                "traceback": traceback.format_exc()
            }
        
        return result

# Global executor instance
executor = PlaywrightExecutor()

@app.route('/web', methods=['GET'])
def web_interface():
    """Web interface for testing the API"""
    # Use the default example from simple_navigation
    default_code = """
# Example: Navigate to a website and get its title
await page.goto('https://www.w3schools.com/html/html_page_title.asp')
title = await page.title()
url = page.url
result = {
    'title': title,
    'url': url,
    'success': True
}
return result
"""
    return render_template('index.html', default_code=default_code)

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        "message": "Playwright Generic Executor API",
        "version": "1.0.0",
        "web_interface": "/web",
        "endpoints": {
            "/execute": {
                "method": "POST",
                "description": "Execute Playwright code",
                "parameters": {
                    "code": "Python code string (required)",
                    "browser_options": "Browser launch options (optional)",
                    "context_options": "Browser context options (optional)"
                }
            },
            "/examples": {
                "method": "GET", 
                "description": "Get example code snippets"
            },
            "/web": {
                "method": "GET",
                "description": "Web interface for testing"
            }
        }
    })

@app.route('/execute', methods=['POST'])
def execute_playwright():
    """Execute Playwright code endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({
                "success": False,
                "error": {
                    "message": "Missing 'code' parameter in request body",
                    "type": "ValidationError"
                }
            }), 400
        
        code = data['code']
        browser_options = data.get('browser_options', {})
        context_options = data.get('context_options', {})
        
        # Run the async executor
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                executor.execute_code(code, browser_options, context_options)
            )
        finally:
            loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "message": str(e),
                "type": type(e).__name__,
                "traceback": traceback.format_exc()
            }
        }), 500

@app.route('/examples', methods=['GET'])
def get_examples():
    """Get example code snippets"""
    examples = {
        "simple_navigation": {
            "description": "Navigate to a webpage and get title",
            "code": """
# Example: Navigate to a website and get its title
await page.goto('https://www.w3schools.com/html/html_page_title.asp')
title = await page.title()
url = page.url
result = {
    'title': title,
    'url': url,
    'success': True
}
return result
"""
        },
        "screenshot": {
            "description": "Take a screenshot of a webpage",
            "code": """
await page.goto('https://www.w3schools.com/')
screenshot = await page.screenshot()
result = {'screenshot_size': len(screenshot), 'url': page.url}
return result
"""
        },
        "form_interaction": {
            "description": "Fill out and submit a form",
            "code": """
await page.goto('https://www.w3schools.com/html/html_forms.asp')
await page.fill('input[name=\"firstname\"]', 'John')
await page.fill('input[name=\"lastname\"]', 'Doe')
await page.click('input[type=\"submit\"]')
await page.wait_for_load_state('networkidle')
result = {'final_url': page.url, 'success': True}
return result
"""
        },
        "scraping": {
            "description": "Scrape data from a webpage",
            "code": """
await page.goto('https://www.w3schools.com/html/html_tables.asp')
rows = await page.locator('#customers tr').all()
result = []
for row in rows[1:4]:  # Get first 3 data rows
    cells = await row.locator('td').all()
    if len(cells) >= 2:
        company = await cells[0].inner_text()
        contact = await cells[1].inner_text()
        result.append({'company': company, 'contact': contact})
return result
"""
        },
        "wait_for_element": {
            "description": "Wait for an element to appear",
            "code": """
await page.goto('https://www.w3schools.com/')
await page.wait_for_selector('h1')
heading = await page.locator('h1').inner_text()
result = {'heading': heading, 'found': True}
return result
"""
        }
    }
    
    return jsonify({
        "examples": examples,
        "usage_notes": [
            "Use 'page' variable to interact with the browser page",
            "Use 'context' variable for browser context operations", 
            "Use 'browser' variable for browser-level operations",
            "Set 'result' variable to return data from your code",
            "Use 'await' for async operations",
            "Available modules: asyncio, json"
        ]
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": app.config.get('startup_time', 'unknown')
    })

if __name__ == '__main__':
    import time
    app.config['startup_time'] = time.time()
    app.run(debug=True, host='0.0.0.0', port=5001)

# Plain AWS Lambda handler for direct invocation (no API Gateway, no Mangum)
def lambda_handler(event, context=None):
    code = event.get('code')
    browser_options = event.get('browser_options', {})
    context_options = event.get('context_options', {})
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(
            executor.execute_code(code, browser_options, context_options)
        )
    finally:
        loop.close()
    return result
