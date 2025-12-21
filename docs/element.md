# Element

The `Element` class represents a DOM element and provides methods for interaction.

## Getting Elements

Elements are obtained through Tab methods:

```python
element = await tab.find("button")
elements = await tab.find_all("a")
element = await tab.wait_for_selector(".result")
```

---

## Clicking

### `click()`

Click the element with human-like mouse movement.

```python
await element.click()
```

**Features:**
- Scrolls element into view
- Uses Bezier curve mouse movement
- Clicks at random point within element
- Adds realistic timing

**Example:**
```python
button = await tab.find("button.submit")
await button.click()
```

---

## Typing

### `type(text, delay)`

Type text into an input element.

```python
await element.type(text, delay=0.05)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | str | required | Text to type |
| `delay` | float | 0.05 | Delay between keystrokes (randomized ±50%) |

**Example:**
```python
input = await tab.find("input[name='email']")
await input.type("user@example.com")

# Faster typing
await input.type("hello", delay=0.01)
```

---

## Text & HTML

### `text()`

Get the text content of the element.

```python
text = await element.text()
```

**Example:**
```python
heading = await tab.find("h1")
title = await heading.text()
print(title)  # "Example Domain"
```

### `inner_html()`

Get the inner HTML of the element.

```python
html = await element.inner_html()
```

---

## Attributes

### `get_attribute(name)`

Get an attribute value.

```python
value = await element.get_attribute(name)
```

**Example:**
```python
link = await tab.find("a")
href = await link.get_attribute("href")
```

### `set_attribute(name, value)`

Set an attribute value.

```python
await element.set_attribute(name, value)
```

---

## Visibility

### `is_visible()`

Check if the element is visible.

```python
visible = await element.is_visible()
```

**Returns:** `bool`

**Example:**
```python
modal = await tab.find(".modal")
if await modal.is_visible():
    await modal.find("button.close").click()
```

---

## Focus & Scroll

### `focus()`

Focus the element.

```python
await element.focus()
```

### `scroll_into_view()`

Scroll the element into view.

```python
await element.scroll_into_view()
```

---

## OOP Iframe Support

Elements found in OOP (out-of-process) iframes work seamlessly:

```python
# This works even for Cloudflare Turnstile!
checkbox = await tab.find("input[type='checkbox']")
await checkbox.click()  # Click coordinates are calculated correctly
```

**How it works:**
- gdnium automatically detects OOP iframes
- Element coordinates are converted to main page coordinates
- Click events are dispatched to the correct position
