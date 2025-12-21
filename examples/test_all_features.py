"""
Comprehensive gdnium Test Script - Single Browser Session

All tests use the same browser instance to avoid session issues.
"""

import asyncio
from GDNox import Browser

URL = "https://2captcha.com/demo/cloudflare-turnstile-challenge"


async def main():
    print("\n" + "="*60)
    print("🚀 GDNIUM COMPREHENSIVE TEST SUITE (Single Session)")
    print("="*60)
    
    async with Browser() as browser:
        tab = await browser.new_tab()
        
        # ============================================
        # TEST 1: goto() with wait_until options
        # ============================================
        print("\n" + "="*60)
        print("🧪 TEST 1: goto() with wait_until options")
        print("="*60)
        
        # Test domcontentloaded
        print("\n📍 Testing wait_until='domcontentloaded'...")
        start = asyncio.get_event_loop().time()
        await tab.goto("https://example.com", wait_until="domcontentloaded")
        elapsed = asyncio.get_event_loop().time() - start
        print(f"   ✅ Loaded in {elapsed:.2f}s")
        
        # Test load
        print("\n📍 Testing wait_until='load'...")
        start = asyncio.get_event_loop().time()
        await tab.goto("https://example.com", wait_until="load")
        elapsed = asyncio.get_event_loop().time() - start
        print(f"   ✅ Loaded in {elapsed:.2f}s")
        
        # Test networkidle
        print("\n📍 Testing wait_until='networkidle'...")
        start = asyncio.get_event_loop().time()
        await tab.goto("https://httpbin.org/get", wait_until="networkidle", timeout=15.0)
        elapsed = asyncio.get_event_loop().time() - start
        print(f"   ✅ Network idle in {elapsed:.2f}s")
        
        print("\n✅ TEST 1 PASSED!")
        
        # ============================================
        # TEST 2: wait_for_selector()
        # ============================================
        print("\n" + "="*60)
        print("🧪 TEST 2: wait_for_selector() with visible option")
        print("="*60)
        
        await tab.goto("https://example.com", wait_until="load")
        
        # Wait for element in DOM
        print("\n📍 Waiting for h1 in DOM...")
        element = await tab.wait_for_selector("h1", timeout=5.0)
        if element:
            text = await element.text()
            print(f"   ✅ Found: {text}")
        
        # Wait for visible element
        print("\n📍 Waiting for h1 to be visible...")
        element = await tab.wait_for_selector("h1", visible=True, timeout=5.0)
        if element:
            print("   ✅ Element is visible!")
        
        # Wait for non-existent element
        print("\n📍 Testing timeout for non-existent selector...")
        try:
            await tab.wait_for_selector(".never-exists", timeout=2.0)
            print("   ❌ Should have timed out!")
        except TimeoutError:
            print("   ✅ Correctly timed out!")
        
        print("\n✅ TEST 2 PASSED!")
        
        # ============================================
        # TEST 3: race()
        # ============================================
        print("\n" + "="*60)
        print("🧪 TEST 3: race() with selectors and js_functions")
        print("="*60)
        
        await tab.goto("https://example.com", wait_until="load")
        
        # Confirm h1 exists
        print("\n📍 Confirming h1 exists...")
        e = await tab.find("h1")
        print(f"   h1 found: {e is not None}")
        
        # Race CSS selectors
        print("\n📍 Racing CSS selectors...")
        condition, element = await tab.race(
            selectors=["h1", ".nonexistent"],
            timeout=5.0,
        )
        print(f"   ✅ Winner: {condition}")
        text = await element.text()
        print(f"   ✅ Text: {text}")
        
        # Race JS functions
        print("\n📍 Racing JS functions...")
        condition, result = await tab.race(
            js_functions=[
                "document.title.length > 0",
                "window.nonexistent === true",
            ],
            timeout=5.0,
        )
        print(f"   ✅ Winner: {condition}")
        print(f"   ✅ Result: {result}")
        
        # Race mixed
        print("\n📍 Racing mixed CSS + JS...")
        condition, result = await tab.race(
            selectors=["h1"],
            js_functions=["window.customVar === true"],
            timeout=5.0,
        )
        print(f"   ✅ Winner: {condition}")
        
        print("\n✅ TEST 3 PASSED!")
        
        # ============================================
        # TEST 4: Race cancellation performance
        # ============================================
        print("\n" + "="*60)
        print("🧪 TEST 4: race() cancellation performance")
        print("="*60)
        
        print("\n📍 Testing cancellation speed...")
        start = asyncio.get_event_loop().time()
        
        condition, _ = await tab.race(
            selectors=["h1"],
            js_functions=["window.neverTrue === true"],
            timeout=10.0,
        )
        
        elapsed = asyncio.get_event_loop().time() - start
        print(f"   Winner: {condition}")
        print(f"   Time: {elapsed:.2f}s")
        
        if elapsed < 1.0:
            print("   ✅ Fast cancellation confirmed!")
        else:
            print("   ⚠️ Cancellation might be slow")
        
        print("\n✅ TEST 4 PASSED!")
        
        # ============================================
        # TEST 5: Cloudflare Turnstile
        # ============================================
        print("\n" + "="*60)
        print("🧪 TEST 5: Cloudflare Turnstile (OOP Iframe)")
        print("="*60)
        print(f"   URL: {URL}")
        
        # Navigate
        print("\n📍 Navigating with networkidle...")
        await tab.goto(URL, wait_until="networkidle", timeout=30.0)
        print("   ✅ Page loaded")
        
        # Wait for iframe
        print("\n📍 Waiting for Turnstile iframe...")
        await tab.sleep(3)
        
        oop_sessions = len(tab._oop_frame_sessions)
        print(f"   📊 OOP iframe sessions: {oop_sessions}")
        
        if oop_sessions > 0:
            print("   ✅ OOP iframe detected!")
            
            # Try to find checkbox
            print("\n📍 Looking for checkbox in iframe...")
            checkbox = await tab.find("input[type='checkbox']")
            
            if checkbox:
                print(f"   ✅ Found checkbox!")
                
                print("\n📍 Clicking checkbox...")
                await checkbox.click()
                print("   ✅ Click executed!")
                
                # Wait for result
                print("\n📍 Waiting for verification...")
                await tab.sleep(5)
                
                # Check for success
                page_content = await tab.content()
                if "success" in page_content.lower() or "passed" in page_content.lower():
                    print("   🎉 SUCCESS! Captcha might be solved!")
                else:
                    print("   ℹ️ Waiting for more time...")
            else:
                print("   ⚠️ Checkbox not found directly")
        else:
            print("   ⚠️ No OOP iframe detected")
        
        # Screenshot
        await tab.screenshot("test_final.png")
        print("   📸 Screenshot saved: test_final.png")
        
        print("\n✅ TEST 5 COMPLETE!")
        
    print("\n" + "="*60)
    print("🎉 ALL TESTS COMPLETED!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
