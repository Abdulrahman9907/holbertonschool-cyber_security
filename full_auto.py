#!/usr/bin/env python3
"""
Full automation using Playwright without login re-prompts.
Keeps browser alive and finds the correction button to click.
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
        """Push with 'a' commit"""
        subprocess.run(['git', 'add', '-A'], capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'a'], capture_output=True)
        subprocess.run(['git', 'push'], capture_output=True)

    async with async_playwright() as p:
        print("[LAUNCH] Starting browser (keep it open, don't close)...")
        browser = await p.chromium.launch(headless=False)

        # Use persistent context to maintain login
        context = await browser.new_context()
        page = await context.new_page()

        print("[NAV] Opening intranet project...")
        await page.goto("https://intranet.hbtn.io/projects/3118", wait_until="networkidle")

        # Check current URL
        current_url = page.url
        print(f"[URL] {current_url}")

        # If on login page, wait for manual login
        if "sign_in" in current_url:
            print("\n[LOGIN REQUIRED]")
            print("A browser window opened on the login page.")
            print("Complete your Google OAuth login in that window.")
            print("Waiting for successful login (checking page URL)...")

            # Wait for redirect away from sign_in page (up to 5 minutes)
            max_wait = 300  # 5 minutes in seconds
            waited = 0
            while waited < max_wait:
                new_url = page.url
                if "sign_in" not in new_url and "login" not in new_url:
                    print(f"[OK] Login successful! Redirected to: {new_url}")
                    break
                await page.wait_for_timeout(1000)
                waited += 1
                if waited % 10 == 0:
                    print(f"[WAITING] Still waiting... ({waited}s)")

            await page.wait_for_timeout(2000)

        print("\n[PUSH] Pushing code...")
        push_code()

        # Refresh page
        await page.reload(wait_until="networkidle")
        await page.wait_for_timeout(3000)

        print("[CORRECTIONS] Starting test loop...\n")

        for attempt in range(1, 11):
            print(f"[ATTEMPT {attempt}/10] ", end="", flush=True)

            # Take screenshot first to see current state
            await page.screenshot(path=str(project_dir / f"screen_{attempt}_before.png"))

            # Find ALL buttons on page
            all_buttons = await page.query_selector_all("button")
            print(f"(found {len(all_buttons)} buttons) ", end="", flush=True)

            button_to_click = None
            for btn in all_buttons:
                try:
                    text = await btn.inner_text()
                    if text and ("correction" in text.lower() or "run" in text.lower()):
                        button_to_click = btn
                        print(f"Found: '{text[:30]}' ", end="", flush=True)
                        break
                except:
                    pass

            if not button_to_click:
                print("NO BUTTON FOUND")
                await page.screenshot(path=str(project_dir / f"screen_{attempt}_error.png"))

                # Save page HTML for inspection
                html = await page.content()
                with open(project_dir / f"page_{attempt}.html", "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"[SAVED] page_{attempt}.html")
                break

            # Click the button
            try:
                print("CLICKING...", end="", flush=True)
                await button_to_click.click()
                await page.wait_for_timeout(6000)
                print(" DONE", flush=True)
            except Exception as e:
                print(f" ERROR: {str(e)[:40]}", flush=True)

            # Take screenshot after
            await page.screenshot(path=str(project_dir / f"screen_{attempt}_after.png"))

            # Check page content
            body_text = await page.inner_text("body")

            if any(x in body_text.lower() for x in ["success", "passed", "correct", "all test"]):
                print("\n[SUCCESS] Tests passed!")
                break

            elif any(x in body_text.lower() for x in ["error", "failed", "fail", "wrong"]):
                print("[FAILED] Need to fix code")

                # Try to extract error
                try:
                    error_elem = await page.query_selector("[class*='error'], [class*='fail']")
                    if error_elem:
                        error_text = await error_elem.inner_text()
                        print(f"  Error: {error_text[:100]}")
                except:
                    pass

                print("\n[WAITING] Pausing for 30 seconds to allow code fix...")
                for i in range(30):
                    await page.wait_for_timeout(1000)

                print("[PUSHING] Pushing any code changes...")
                push_code()

                # Refresh for next attempt
                await page.reload(wait_until="networkidle")
                await page.wait_for_timeout(3000)
            else:
                print("[UNCLEAR]")

        print("\n[DONE] Automation finished!")
        print("[BROWSER] Browser remains open. Close it when finished checking results.")

        # Keep browser open indefinitely
        await page.wait_for_timeout(999999000)

if __name__ == "__main__":
    print("\n" + "="*70)
    print("HOLBERTON INTRANET - FULL AUTOMATION")
    print("="*70 + "\n")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[EXIT] Automation stopped by user")
