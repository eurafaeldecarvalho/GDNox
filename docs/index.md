# gdnium Documentation

Undetectable browser automation library with stealth features.

## Quick Links

- [Getting Started](getting-started.md) - Installation and basic usage
- [Browser](browser.md) - Browser class and launch options
- [Tab](tab.md) - Page navigation, element finding, JavaScript execution
- [Element](element.md) - Element interactions (click, type, etc.)
- [Network](network.md) - Request/response interception
- [Stealth](stealth.md) - Anti-detection features

## Features

- **CDP Direct** - Connects to Chrome via Chrome DevTools Protocol (no WebDriver)
- **Closed Shadow Root Access** - Access elements inside closed shadow DOMs
- **OOP Iframe Support** - Find and click elements in cross-origin iframes (Cloudflare Turnstile)
- **Stealth Mode** - Auto-seeds history, cookies, bypasses bot detection
- **Human-like Behavior** - Bezier curve mouse movements, randomized timing
- **Network Interception** - Monitor, modify, or block requests

## Quick Example

```python
import asyncio
from GDNox import Browser

async def main():
    async with Browser() as browser:
        tab = await browser.new_tab()
        
        # Navigate with network idle wait
        await tab.goto("https://example.com", wait_until="networkidle")
        
        # Find and click element
        button = await tab.find("button.submit")
        await button.click()
        
        # Wait for result
        result = await tab.wait_for_selector(".success", visible=True)
        print(await result.text())

asyncio.run(main())
```

## Requirements

- Python 3.10+
- Google Chrome or Chromium installed
