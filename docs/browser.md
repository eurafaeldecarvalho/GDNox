# Browser

The `Browser` class manages the Chrome browser instance.

## Constructor

```python
Browser(
    chrome_path: str = None,       # Path to Chrome (auto-detected if None)
    headless: bool = False,        # Run headless (NOT recommended for stealth)
    user_data_dir: str = None,     # Chrome profile directory
    proxy: str = None,             # Proxy server URL
    extra_args: List[str] = None,  # Additional Chrome arguments
    auto_seed: bool = True,        # Auto-seed history/cookies for stealth
)
```

## Parameters

### `chrome_path`
Path to Chrome executable. If not provided, gdnium auto-detects Chrome on your system.

```python
Browser(chrome_path="/usr/bin/google-chrome")
```

### `headless`
Run Chrome in headless mode. **Not recommended** for stealth as many sites detect headless browsers.

```python
Browser(headless=True)  # Headless mode
```

### `user_data_dir`
Path to Chrome profile directory. Use this to:
- Persist cookies and sessions
- Use an existing Chrome profile
- Share data between runs

```python
Browser(user_data_dir="/path/to/profile")
```

If not provided, a temporary profile is created and deleted on close.

### `proxy`
Proxy server to use for all requests. **Supports authentication** via URL format.

```python
# Without authentication
Browser(proxy="http://127.0.0.1:8080")

# With authentication (user:password@host:port)
Browser(proxy="http://user:password@proxy.example.com:8080")

# SOCKS5 proxy
Browser(proxy="socks5://127.0.0.1:1080")
```

**Note:** Proxy authentication is handled automatically via CDP. WebRTC leak protection is enabled by default to prevent IP leaks when using proxies.

### `extra_args`
Additional Chrome command line arguments.

```python
Browser(extra_args=["--disable-gpu", "--no-sandbox"])
```

### `auto_seed`
Automatically seed browser history and cookies for stealth. Only applies to **temporary profiles** (when `user_data_dir` is not provided).

```python
Browser(auto_seed=True)   # Seed history/cookies (default)
Browser(auto_seed=False)  # Don't seed
```

## Methods

### `launch()`
Launch the browser. Called automatically when using `async with`.

```python
browser = Browser()
await browser.launch()
# ... use browser ...
await browser.close()
```

### `close()`
Close the browser and cleanup.

```python
await browser.close()
```

### `new_tab()`
Create a new tab.

```python
tab = await browser.new_tab()
```

**Returns:** `Tab` instance

## Context Manager

The recommended way to use Browser:

```python
async with Browser() as browser:
    tab = await browser.new_tab()
    # ... browser closes automatically
```

## Stealth Features

When `auto_seed=True` and using a temporary profile, gdnium automatically:

1. **Seeds browsing history** with 40+ popular sites (Google, YouTube, Facebook, Amazon, etc.)
2. **Seeds cookies** for major websites (Google, YouTube, Facebook, Twitter, etc.)

This makes the browser profile look like a real user's browser.
