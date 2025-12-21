"""
Test: Click the Turnstile checkbox and check if captcha is bypassed.
"""

import asyncio
from GDNox import Browser


async def main():
    print("🔍 Test: Click Turnstile checkbox and verify bypass")
    print("Target: https://2captcha.com/demo/cloudflare-turnstile-challenge\n")
    
    async with Browser(headless=False) as browser:
        tab = await browser.new_tab()
        
        await tab.goto("https://2captcha.com/demo/cloudflare-turnstile-challenge")
        print("✅ Page loaded")
        
        # Wait for Turnstile to initialize
        print("⏳ Waiting 5s for Turnstile initialization...")
        await tab.sleep(5)
        
        print(f"\n📊 OOP frame sessions: {len(tab._oop_frame_sessions)}")
        
        # Find the checkbox
        print("\n🔎 Looking for checkbox...")
        checkbox = await tab.find("input[type=checkbox]", timeout=10)
        
        if not checkbox:
            print("❌ Checkbox not found!")
            input("Press Enter to close...")
            return
        
        print(f"✅ Found checkbox! Node ID: {checkbox.node_id}")
        print(f"   Session ID: {checkbox._session_id[:30] if checkbox._session_id else 'None'}...")
        
        # Take screenshot before click
        await tab.screenshot("before_click.png")
        print("📸 Screenshot saved: before_click.png")
        
        # Click the checkbox
        print("\n🖱️ Clicking checkbox...")
        try:
            await checkbox.click()
            print("✅ Click executed!")
        except Exception as e:
            print(f"❌ Click failed: {e}")
            
            # Try alternative: click by coordinates
            print("\n🔄 Trying coordinate-based click...")
            try:
                # Get box model
                box = await checkbox._get_box_model()
                if box:
                    content = box.get("content", [])
                    if len(content) >= 4:
                        x = (content[0] + content[2]) / 2
                        y = (content[1] + content[5]) / 2
                        print(f"   Coordinates: ({x}, {y})")
                        
                        await tab._cdp.send("Input.dispatchMouseEvent", {
                            "type": "mousePressed",
                            "x": x, "y": y,
                            "button": "left",
                            "clickCount": 1,
                        })
                        await tab._cdp.send("Input.dispatchMouseEvent", {
                            "type": "mouseReleased",
                            "x": x, "y": y,
                            "button": "left",
                            "clickCount": 1,
                        })
                        print("✅ Coordinate click executed!")
            except Exception as e2:
                print(f"❌ Coordinate click also failed: {e2}")
        
        # Wait for verification
        print("\n⏳ Waiting 5s for verification...")
        await tab.sleep(5)
        
        # Take screenshot after click
        await tab.screenshot("after_click.png")
        print("📸 Screenshot saved: after_click.png")
        
        # Check if captcha was solved
        print("\n🔍 Checking captcha status...")
        
        # Try to find success indicator
        success_response = await tab.find("input[name='cf-turnstile-response']", timeout=2)
        if success_response:
            try:
                value = await success_response.get_attribute("value")
                if value and len(value) > 10:
                    print(f"🎉 CAPTCHA SOLVED! Token received ({len(value)} chars)")
                else:
                    print(f"⚠️ Response field exists but empty/short")
            except Exception:
                print("⚠️ Could not read response value")
        
        # Check page content for success message
        try:
            body = await tab.find("body", timeout=2)
            if body:
                text = await body.text()
                if "success" in text.lower() or "solved" in text.lower():
                    print("🎉 SUCCESS indicator found in page!")
                elif "challenge" in text.lower():
                    print("⚠️ Challenge still active")
        except Exception:
            pass
        
        print("\n" + "="*50)
        input("Press Enter to close browser...")


if __name__ == "__main__":
    asyncio.run(main())
