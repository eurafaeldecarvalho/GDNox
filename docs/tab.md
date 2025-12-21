# Tab

The `Tab` class represents a browser tab and provides methods for navigation, element finding, and JavaScript execution.

## Navigation

### `goto(url, wait_until, timeout)`

Navigate to a URL.

```python
await tab.goto(url, wait_until="load", timeout=30.0)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | str | required | URL to navigate to |
| `wait_until` | str | "load" | Wait condition (see below) |
| `timeout` | float | 30.0 | Maximum wait time in seconds |

**wait_until options:**
| Value | Description |
|-------|-------------|
| `"load"` | Wait for `load` event (default) |
| `"domcontentloaded"` | Wait for DOM to be ready (faster) |
| `"networkidle"` | Wait until ≤2 network connections for 500ms |
| `"networkidle0"` | Wait until 0 network connections for 500ms |
| `"networkidle2"` | Same as `networkidle` |

**Examples:**
```python
# Default - wait for load event
await tab.goto("https://example.com")

# Fast - just wait for DOM
await tab.goto("https://example.com", wait_until="domcontentloaded")

# SPAs - wait for network to be quiet
await tab.goto("https://spa-app.com", wait_until="networkidle")
```

---

## Element Finding

### `find(selector)`

Find a single element by CSS selector. Searches main DOM, shadow roots, and OOP iframes.

```python
element = await tab.find(selector)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `selector` | str | CSS selector |

**Returns:** `Element` or `None`

**Examples:**
```python
# Find by class
button = await tab.find(".submit-button")

# Find by ID
form = await tab.find("#login-form")

# Find by attribute
input = await tab.find("input[type='email']")

# Works in shadow roots and iframes!
checkbox = await tab.find("input[type='checkbox']")
```

### `find_all(selector)`

Find all matching elements.

```python
elements = await tab.find_all(selector)
```

**Returns:** `List[Element]`

**Example:**
```python
links = await tab.find_all("a.nav-link")
for link in links:
    print(await link.text())
```

---

## Waiting

### `wait_for_selector(selector, visible, hidden, timeout)`

Wait for an element to appear in the DOM.

```python
element = await tab.wait_for_selector(selector, visible=False, hidden=False, timeout=30.0)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `selector` | str | required | CSS selector |
| `visible` | bool | False | Wait for element to be visible |
| `hidden` | bool | False | Wait for element to disappear |
| `timeout` | float | 30.0 | Maximum wait time |

**Returns:** `Element` or `None` (if hidden=True)

**Raises:** `TimeoutError` if not found within timeout

**Examples:**
```python
# Wait for element in DOM
element = await tab.wait_for_selector(".result")

# Wait for element to be VISIBLE
element = await tab.wait_for_selector(".modal", visible=True)

# Wait for loading spinner to disappear
await tab.wait_for_selector(".loading", hidden=True)
```

### `wait_for_function(expression, timeout, poll_interval)`

Wait for a JavaScript expression to return truthy.

```python
result = await tab.wait_for_function(expression, timeout=30.0, poll_interval=0.1)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `expression` | str | required | JavaScript expression |
| `timeout` | float | 30.0 | Maximum wait time |
| `poll_interval` | float | 0.1 | Time between checks |

**Returns:** The truthy result

**Examples:**
```python
# Wait for variable
await tab.wait_for_function("window.dataLoaded === true")

# Wait for element count
await tab.wait_for_function("document.querySelectorAll('.item').length > 5")
```

### `race(selectors, js_functions, visible, timeout)`

Race multiple conditions - return the first one that resolves.

```python
condition, result = await tab.race(
    selectors=["selector1", "selector2"],
    js_functions=["js_expression1"],
    visible=False,
    timeout=30.0
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `selectors` | List[str] | None | CSS selectors to race |
| `js_functions` | List[str] | None | JS expressions to race |
| `visible` | bool | False | Wait for visible elements |
| `timeout` | float | 30.0 | Maximum wait time |

**Returns:** `tuple[str, Any]` - (winning_condition, result)
- For CSS selectors: result is `Element`
- For JS expressions: result is the truthy value

**Examples:**
```python
# Race multiple selectors
condition, element = await tab.race(
    selectors=[".success", ".error", "#captcha-failed"],
)

if condition == ".success":
    print("Success!")
elif condition == ".error":
    print("Error:", await element.text())

# Mixed race
condition, result = await tab.race(
    selectors=[".done"],
    js_functions=["window.completed === true"],
)
```

---

## JavaScript

### `evaluate(expression)`

Execute JavaScript and return the result.

```python
result = await tab.evaluate(expression)
```

**Returns:** JavaScript result (converted to Python types)

**Examples:**
```python
# Get value
title = await tab.evaluate("document.title")

# Complex expression
data = await tab.evaluate("""
    (() => {
        return {
            url: window.location.href,
            cookies: document.cookie,
            height: document.body.scrollHeight
        }
    })()
""")
```

---

## Cookies & Storage

### `set_cookies(cookies)`

Set cookies for the current page.

```python
await tab.set_cookies([
    {"name": "session", "value": "abc123", "domain": ".example.com"},
])
```

### `get_cookies(urls)`

Get cookies.

```python
cookies = await tab.get_cookies()
cookies = await tab.get_cookies(urls=["https://example.com"])
```

### `clear_cookies()`

Clear all cookies.

```python
await tab.clear_cookies()
```

### `set_local_storage(origin, items)`

Set local storage items.

```python
await tab.set_local_storage("https://example.com", {
    "key": "value",
    "another": "data"
})
```

### `get_local_storage()`

Get all local storage items.

```python
items = await tab.get_local_storage()
```

---

## Other Methods

### `content()`

Get page HTML content.

```python
html = await tab.content()
```

### `screenshot(path, full_page)`

Take a screenshot.

```python
# Save to file
await tab.screenshot("screenshot.png")

# Full page screenshot
await tab.screenshot("full.png", full_page=True)

# Get as bytes
data = await tab.screenshot()
```

### `sleep(seconds)`

Wait for a randomized amount of time (±50% of specified value).

```python
await tab.sleep(5)  # Waits 2.5 to 7.5 seconds
```

### `close()`

Close the tab.

```python
await tab.close()
```

---

## Network Property

Access network interception features.

```python
@tab.network.on('request')
async def on_request(request):
    print(request.url)
```

See [Network](network.md) for full documentation.
