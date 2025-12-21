# Stealth Features

gdnium includes built-in stealth features to make automated browsers undetectable.

## Auto-Seeding

When using a temporary profile (no `user_data_dir`), gdnium automatically seeds:

### Browser History

Seeds visits to 40+ popular sites:

**Global/US:**
- Google, YouTube, Facebook, Twitter/X
- Amazon, Netflix, Instagram, TikTok
- LinkedIn, Reddit, Wikipedia
- GitHub, StackOverflow

**Brazil:**
- Google.com.br, Mercado Livre
- Globo, UOL, Folha
- iFood, Banco do Brasil

### Cookies

Seeds realistic cookies for major sites:

| Site | Cookies |
|------|---------|
| Google | NID, 1P_JAR, CONSENT, SID |
| YouTube | PREF, VISITOR_INFO1_LIVE |
| Facebook | datr, fr, sb |
| Twitter | guest_id, ct0 |
| Amazon | session-id, ubid |
| And many more... |

## Disable Auto-Seeding

```python
Browser(auto_seed=False)
```

## Human-like Mouse

gdnium uses realistic mouse movements:

- **Bezier curves** for natural trajectories
- **Micro-jitter** (0.5px random variation)
- **Acceleration/deceleration** (ease-out cubic)
- **Overshoot correction** sometimes overshoots and corrects
- **Variable timing** between movements

```python
# Automatic human-like movement
await element.click()
```

## Randomized Sleep

The `sleep()` function automatically randomizes timing:

```python
await tab.sleep(5)  # Actually waits 2.5 to 7.5 seconds (±50%)
```

## Closed Shadow Root Access

gdnium can access elements inside closed shadow roots:

```python
# Works even with shadow-root (mode: closed)
element = await tab.find(".button-inside-shadow-root")
```

## OOP Iframe Support

Cross-origin (out-of-process) iframes are automatically detected and handled:

```python
# Works with Cloudflare Turnstile!
checkbox = await tab.find("input[type='checkbox']")
await checkbox.click()
```

## No WebDriver

gdnium connects directly via Chrome DevTools Protocol (CDP), not WebDriver:

- No `navigator.webdriver` detection
- No WebDriver-related Chrome flags
- More control over stealth

## WebRTC Leak Prevention

When using proxies, gdnium prevents WebRTC IP leaks:

- `--disable-webrtc` flag enabled
- `--webrtc-ip-handling-policy=disable_non_proxied_udp`
- Sites cannot detect your real IP via WebRTC

```python
# Proxied traffic protected from WebRTC leaks
Browser(proxy="http://user:pass@proxy.example.com:8080")
```

## Profile Persistence

For long-running bots, use a persistent profile:

```python
async with Browser(user_data_dir="/path/to/profile") as browser:
    # Profile is preserved between runs
    # Cookies, history, local storage all persist
    ...
```

## Best Practices

1. **Don't use headless mode** - Many sites detect headless browsers
   ```python
   Browser(headless=False)  # Good
   ```

2. **Use networkidle for SPAs** - Waits for all requests to complete
   ```python
   await tab.goto(url, wait_until="networkidle")
   ```

3. **Add random delays** - Use `sleep()` between actions
   ```python
   await tab.sleep(2)  # Randomized to 1-3 seconds
   ```

4. **Use persistent profiles** - For sites that track sessions
   ```python
   Browser(user_data_dir="/path/to/profile")
   ```

5. **Don't rush** - Human users are slow, add delays between actions
