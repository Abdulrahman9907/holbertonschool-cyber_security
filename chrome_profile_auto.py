#!/usr/bin/env python3
"""
Automation using your existing Chrome profile (with saved login).
No re-authentication needed - uses your Chrome cookies.
"""

import asyncio
import os
import subprocess
from pathlib import Path

project_dir = Path(r"C:\Users\Admin\Documents\projects\holbertonschool-cyber_security")
os.chdir(project_dir)

async def main():
    from playwright.async_api import async_playwright

    def push_code():
        subprocess.run(['git', 'add', '-A'], capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'a'], capture_output=True)
        subprocess.run(['git', 'push'], capture_output=True)

    async with async_playwright() as p:
        print("[CONNECT] Using existing Chrome profile...")

        # Use persistent context with Chrome profile
        chrome_user_data = r"C:\Users\Admin\AppData\Local\Google\Chrome\User Data"

        context = await p.chromium.launch_persistent_context(
            user_data_dir=chrome_user_data,
            headless=False,
            bypass_csp=True,
        )

        page = await context.new_page()

        print("[NAV] Opening project page...")
        await page.goto("https://intranet.hbtn.io/projects/3118", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        current_url = page.url
        print(f"[URL] {current_url}")

        # Check if still need login
        if "sign_in" in current_url or "login" in current_url:
            print("[ERROR] Chrome profile not authenticated. You need to log in first manually.")
            print("[ACTION] Please:")
            print("  1. Open Chrome manually")
            print("  2. Go to https://intranet.hbtn.io")
            print("  3. Complete Google OAuth login")
            print("  4. Return here and try again")
            await context.close()
            return

        print("[OK] Authenticated with Chrome profile!\n")

        # Push code
        print("[PUSH] Pushing code with commit 'a'...")
        push_code()
        print("[PUSHED] Code is live\n")

        # Refresh page
        await page.reload(wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Correction loop
        print("[CORRECTIONS] Starting automated test loop...\n")

        success = False
        for attempt in range(1, 11):
            print(f"[ATTEMPT {attempt}/10] ", end="", flush=True)

            # Find correction button
            all_buttons = await page.query_selector_all("button")
            button_to_click = None

            for btn in all_buttons:
                try:
                    text = await btn.inner_text()
                    if text and "correction" in text.lower():
                        button_to_click = btn
                        break
                except:
                    pass

            if not button_to_click:
                print("NO BUTTON - checking page...")
                await page.screenshot(path=str(project_dir / f"final_state_{attempt}.png"))
                break

            # Click button
            try:
                print("RUNNING...", end="", flush=True)
                await button_to_click.click()
                await page.wait_for_timeout(6000)
            except Exception as e:
                print(f"ERROR: {e}")
                continue

            # Check results
            body_text = await page.inner_text("body")

            # Success check
            if any(x in body_text.lower() for x in ["all test passed", "success", "all passed", "100%"]):
                print(" SUCCESS!")
                await page.screenshot(path=str(project_dir / "SUCCESS.png"))
                success = True
                break

            # Failure check
            elif any(x in body_text.lower() for x in ["error", "failed", "fail", "wrong", "incorrect"]):
                print(" FAILED - fixing...")

                # Try to get error details
                try:
                    errors = await page.query_selector_all("[class*='error']")
                    for e in errors[:1]:
                        text = await e.inner_text()
                        if text:
                            print(f"\n  Error: {text[:80]}")
                except:
                    pass

                await page.screenshot(path=str(project_dir / f"error_{attempt}.png"))

                # Wait for code fix (30 seconds)
                print("  [Waiting for code fix...]")
                await page.wait_for_timeout(30000)

                # Push fixes
                print("  [Pushing fixes...]")
                push_code()

                # Refresh
                await page.reload(wait_until="networkidle")
                await page.wait_for_timeout(3000)
                print()

            else:
                print(" checking...")
                await page.wait_for_timeout(2000)

        # Summary
        print("\n" + "="*60)
        if success:
            print("RESULT: PROJECT PASSED!")
        else:
            print("RESULT: Check browser for status")
        print("="*60)

        await page.wait_for_timeout(10000)
        await context.close()

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CHROME PROFILE AUTOMATION")
    print("="*70 + "\n")

    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
