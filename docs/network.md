# Network Interception

gdnium provides powerful network interception capabilities through the `tab.network` interface.

## Quick Start

```python
async with Browser() as browser:
    tab = await browser.new_tab()
    
    # Monitor requests
    @tab.network.on('request')
    async def on_request(request):
        print(f"Request: {request.url}")
    
    # Monitor responses
    @tab.network.on('response')
    async def on_response(response):
        print(f"Response: {response.status} {response.url}")
    
    await tab.goto("https://example.com")
```

---

## Monitoring Events

### `@network.on('request')`

Called when a request is sent. **Does not pause the request.**

```python
@tab.network.on('request')
async def on_request(request):
    print(f"📤 {request.method} {request.url}")
    print(f"   Headers: {request.headers}")
    print(f"   Type: {request.resource_type}")
```

**Request Properties:**
| Property | Type | Description |
|----------|------|-------------|
| `url` | str | Request URL |
| `method` | str | HTTP method (GET, POST, etc.) |
| `headers` | dict | Request headers |
| `post_data` | str | POST body (if any) |
| `resource_type` | str | Type (Document, Script, Image, etc.) |

### `@network.on('response')`

Called when a response is received.

```python
@tab.network.on('response')
async def on_response(response):
    print(f"📥 {response.status} {response.url}")
    
    # Get response body
    body = await response.body()
    print(f"   Body length: {len(body)}")
    
    # Or as JSON
    data = await response.json()
```

**Response Properties:**
| Property | Type | Description |
|----------|------|-------------|
| `url` | str | Response URL |
| `status` | int | HTTP status code |
| `status_text` | str | Status text |
| `headers` | dict | Response headers |
| `mime_type` | str | MIME type |

**Response Methods:**
| Method | Returns | Description |
|--------|---------|-------------|
| `body()` | str | Get response body as string |
| `json()` | Any | Parse body as JSON |

### `@network.on('finished')`

Called when a request finishes loading.

```python
@tab.network.on('finished')
async def on_finished(request_id):
    print(f"Finished: {request_id}")
```

### `@network.on('failed')`

Called when a request fails.

```python
@tab.network.on('failed')
async def on_failed(request_id, error):
    print(f"Failed: {request_id} - {error}")
```

---

## Intercepting Requests

### `@network.intercept(pattern)`

Intercept requests matching a pattern. **The request is PAUSED** until you call one of:
- `request.continue_()` - Continue normally
- `request.abort()` - Block the request
- `request.respond(...)` - Return a fake response

```python
@tab.network.intercept('*api.example.com*')
async def intercept(request):
    if '/blocked' in request.url:
        await request.abort()
    else:
        await request.continue_()
```

**Pattern Syntax:**
- `*` matches any characters
- `?` matches single character
- Example: `*api.example.com*` matches any URL containing "api.example.com"

---

## Request Actions

### `request.continue_(url, method, headers, post_data)`

Continue the request, optionally modifying it.

```python
@tab.network.intercept('*')
async def intercept(request):
    # Continue with modified headers
    await request.continue_(
        headers={"X-Custom": "value", **request.headers}
    )
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | str | Override URL |
| `method` | str | Override method |
| `headers` | dict | Override headers |
| `post_data` | str | Override POST body |

### `request.abort(reason)`

Abort the request.

```python
@tab.network.intercept('*ads*')
async def block_ads(request):
    await request.abort("BlockedByClient")
```

**Reason options:**
- `"Failed"`
- `"Aborted"`
- `"TimedOut"`
- `"AccessDenied"`
- `"ConnectionClosed"`
- `"ConnectionReset"`
- `"ConnectionRefused"`
- `"ConnectionAborted"`
- `"ConnectionFailed"`
- `"NameNotResolved"`
- `"InternetDisconnected"`
- `"AddressUnreachable"`
- `"BlockedByClient"`
- `"BlockedByResponse"`

### `request.respond(status, headers, body, json_data)`

Return a fake response.

```python
@tab.network.intercept('*api/data*')
async def fake_response(request):
    await request.respond(
        status=200,
        json_data={"fake": "data", "success": True}
    )
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | int | HTTP status code (default: 200) |
| `headers` | dict | Response headers |
| `body` | str | Response body as string |
| `json_data` | Any | Response body as JSON (auto-sets Content-Type) |

---

## Complete Example

```python
import asyncio
from gdnium import Browser

async def main():
    async with Browser() as browser:
        tab = await browser.new_tab()
        
        # Log all API requests
        @tab.network.on('request')
        async def log_api(request):
            if 'api' in request.url:
                print(f"API: {request.method} {request.url}")
        
        # Capture JSON responses
        @tab.network.on('response')
        async def capture_json(response):
            if 'application/json' in response.mime_type:
                data = await response.json()
                print(f"JSON: {data}")
        
        # Block tracking scripts
        @tab.network.intercept('*analytics*')
        async def block_analytics(request):
            await request.abort()
        
        # Mock API responses
        @tab.network.intercept('*api/user*')
        async def mock_user(request):
            await request.respond(json_data={
                "id": 123,
                "name": "Test User"
            })
        
        await tab.goto("https://example.com")

asyncio.run(main())
```
