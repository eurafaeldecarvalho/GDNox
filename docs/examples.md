# Examples

Complete examples for common use cases.

## Basic Web Scraping

```python
import asyncio
from GDNox import Browser

async def scrape_example():
    async with Browser() as browser:
        tab = await browser.new_tab()
        await tab.goto("https://example.com")
        
        # Get page title
        title = await tab.evaluate("document.title")
        
        # Get all links
        links = await tab.find_all("a")
        for link in links:
            href = await link.get_attribute("href")
            text = await link.text()
            print(f"{text}: {href}")

asyncio.run(scrape_example())
```

## Form Submission

```python
async def login():
    async with Browser() as browser:
        tab = await browser.new_tab()
        await tab.goto("https://example.com/login")
        
        # Fill form
        email = await tab.find("input[name='email']")
        await email.type("user@example.com")
        
        password = await tab.find("input[name='password']")
        await password.type("password123")
        
        # Submit
        submit = await tab.find("button[type='submit']")
        await submit.click()
        
        # Wait for result
        condition, result = await tab.race(
            selectors=[".success", ".error"],
            timeout=10.0
        )
        
        if condition == ".success":
            print("Login successful!")
        else:
            print("Login failed:", await result.text())

asyncio.run(login())
```

## Cloudflare Turnstile

```python
async def solve_turnstile():
    async with Browser() as browser:
        tab = await browser.new_tab()
        await tab.goto(
            "https://2captcha.com/demo/cloudflare-turnstile-challenge",
            wait_until="networkidle"
        )
        
        # Wait for iframe to load
        await tab.sleep(3)
        
        # Find checkbox (works in OOP iframe!)
        checkbox = await tab.find("input[type='checkbox']")
        if checkbox:
            await checkbox.click()
            print("Clicked Turnstile checkbox")
            
            # Wait for verification
            await tab.sleep(5)

asyncio.run(solve_turnstile())
```

## Blocking Ads/Trackers

```python
async def block_ads():
    async with Browser() as browser:
        tab = await browser.new_tab()
        
        # Block ad requests
        @tab.network.intercept('*doubleclick*')
        async def block(request):
            await request.abort()
        
        @tab.network.intercept('*googlesyndication*')
        async def block2(request):
            await request.abort()
        
        @tab.network.intercept('*analytics*')
        async def block3(request):
            await request.abort()
        
        await tab.goto("https://example.com")

asyncio.run(block_ads())
```

## API Mocking

```python
async def mock_api():
    async with Browser() as browser:
        tab = await browser.new_tab()
        
        # Mock API response
        @tab.network.intercept('*api/user*')
        async def mock(request):
            await request.respond(json_data={
                "id": 123,
                "name": "Test User",
                "premium": True
            })
        
        await tab.goto("https://app.example.com")

asyncio.run(mock_api())
```

## Capturing Network Data

```python
async def capture_api():
    async with Browser() as browser:
        tab = await browser.new_tab()
        
        api_responses = []
        
        @tab.network.on('response')
        async def capture(response):
            if 'api' in response.url and response.status == 200:
                try:
                    data = await response.json()
                    api_responses.append({
                        'url': response.url,
                        'data': data
                    })
                except:
                    pass
        
        await tab.goto("https://app.example.com", wait_until="networkidle")
        
        print(f"Captured {len(api_responses)} API responses")
        for resp in api_responses:
            print(f"  {resp['url']}")

asyncio.run(capture_api())
```

## Wait for Dynamic Content

```python
async def wait_dynamic():
    async with Browser() as browser:
        tab = await browser.new_tab()
        await tab.goto("https://spa-app.com", wait_until="networkidle")
        
        # Wait for content to load
        await tab.wait_for_function(
            "document.querySelectorAll('.product').length > 10"
        )
        
        # Or wait for specific element
        product = await tab.wait_for_selector(".product-detail", visible=True)
        
        print(await product.text())

asyncio.run(wait_dynamic())
```

## Success or Error Detection

```python
async def detect_result():
    async with Browser() as browser:
        tab = await browser.new_tab()
        await tab.goto("https://example.com/process")
        
        # Race between success and error
        condition, element = await tab.race(
            selectors=[
                ".success-message",
                ".error-message",
                ".validation-error",
                "#captcha-failed"
            ],
            js_functions=[
                "window.processComplete === true"
            ],
            timeout=30.0
        )
        
        if condition == ".success-message":
            print("✅ Success!")
        elif condition == ".error-message":
            print("❌ Error:", await element.text())
        elif condition == ".validation-error":
            print("⚠️ Validation error:", await element.text())
        elif "processComplete" in condition:
            print("✅ Process complete via JS")
        else:
            print("❌ Captcha failed")

asyncio.run(detect_result())
```

## Screenshot and PDF

```python
async def screenshot():
    async with Browser() as browser:
        tab = await browser.new_tab()
        await tab.goto("https://example.com")
        
        # Screenshot visible area
        await tab.screenshot("visible.png")
        
        # Full page screenshot
        await tab.screenshot("fullpage.png", full_page=True)

asyncio.run(screenshot())
```

## Persistent Session

```python
async def persistent_session():
    # Use persistent profile
    async with Browser(user_data_dir="/path/to/profile") as browser:
        tab = await browser.new_tab()
        await tab.goto("https://app.example.com")
        
        # First run: login will be required
        # Subsequent runs: already logged in!

asyncio.run(persistent_session())
```
