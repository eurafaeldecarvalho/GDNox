# Getting Started

## Installation

```bash
pip install gdnium
```

Or with Poetry:

```bash
poetry add gdnium
```

## Basic Usage

```python
import asyncio
from gdnium import Browser

async def main():
    # Launch browser
    async with Browser() as browser:
        # Create new tab
        tab = await browser.new_tab()
        
        # Navigate to page
        await tab.goto("https://example.com")
        
        # Find element
        element = await tab.find("h1")
        
        # Get text
        text = await element.text()
        print(text)

asyncio.run(main())
```

## With Options

```python
async with Browser(
    headless=False,           # Show browser window
    user_data_dir="/path",    # Use existing profile
    auto_seed=True,           # Auto-seed history/cookies (default)
    proxy="http://127.0.0.1:8080",  # Use proxy
) as browser:
    ...
```

## Chrome Path

gdnium auto-detects Chrome. To specify manually:

```python
Browser(chrome_path="/path/to/chrome")
```

## Next Steps

- [Browser](browser.md) - All browser options
- [Tab](tab.md) - Navigation and element finding
- [Network](network.md) - Request interception
