#!/usr/bin/env python3
"""
Full automation for Holberton intranet project submission and correction.
Uses Playwright for clean browser control without headless mode issues.
"""

import asyncio
import os
import sys
import subprocess
import time
from pathlib import Path

# Add project to path
project_dir = Path(r"C:\Users\Admin\Documents\projects\holbertonschool-cyber_security")
os.chdir(project_dir)

async def main():
    from playwright.async_api import async_playwright

    def push_code():
        """Push code with message 'a'"""
        subprocess.run(['git', 'add', '-A'], capture_output=True, cwd=str(project_dir))
        subprocess.run(['git', 'commit', '-m', 'a'], capture_output=True, cwd=str(project_dir))
        subprocess.run(['git', 'push'], capture_output=True, cwd=str(project_dir))

    async with async_playwright() as p:
        # Launch browser in normal mode (not headless)
        print("[LAUNCH] Starting browser...")
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("[NAV] Opening intranet project page...")
        await page.goto("https://intranet.hbtn.io/projects/3118", wait_until="networkidle")

        # Check if we need to login
        try:
            # Wait a bit to see if we're redirected
            await page.wait_for_timeout(3000)

            current_url = page.url
            print(f"[URL] Current: {current_url}")

            if "sign_in" in current_url or "login" in current_url:
                print("[LOGIN] Not authenticated - waiting for Google OAuth login...")
                print("[ACTION] Complete login in the browser window that appeared")

                # Wait for successful redirect to projects page
                try:
                    await page.wait_for_url("**/projects/**", timeout=300000)  # 5 minute timeout
                    print("[OK] Login successful!")
                except:
                    print("[ERROR] Login timeout - please ensure you're logged in")
                    await browser.close()
                    return
            else:
                print("[OK] Already authenticated")
        except Exception as e:
            print(f"[CHECK] {e}")

        # Wait for page to stabilize
        await page.wait_for_timeout(2000)

        # Push code
        print("\n[PUSH] Pushing code with commit 'a'...")
        push_code()
        print("[OK] Code pushed")

        # Refresh page
        await page.reload(wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Correction loop
        print("\n[CORRECTIONS] Starting test loop...\n")

        for attempt in range(1, 11):
            print(f"[ATTEMPT {attempt}/10]", end=" ")
            sys.stdout.flush()

            # Find correction button
            try:
                # Try multiple button selectors
                button = None

                # Try direct text match
                buttons = await page.query_selector_all("button")
                for btn in buttons:
                    text = await btn.inner_text()
                    if "correction" in text.lower():
                        button = btn
                        break

                if not button:
                    print("NO_BUTTON")
                    await page.screenshot(path=str(project_dir / f"attempt_{attempt}.png"))
                    # Print page content for debugging
                    content = await page.content()
                    with open(project_dir / f"page_{attempt}.html", "w") as f:
                        f.write(content)
                    break

                print("CLICKING...", end=" ")
                sys.stdout.flush()

                # Click without scroll (simpler approach)
                await button.click(timeout=10000)
                await page.wait_for_timeout(5000)

            except Exception as e:
                print(f"ERROR: {str(e)[:50]}")
                await page.screenshot(path=str(project_dir / f"error_{attempt}.png"))
                await page.wait_for_timeout(2000)
                continue

            # Check page for results
            page_content = await page.content()
            page_text = await page.inner_text("body")

            # Success indicators
            success_keywords = ["all tests passed", "success", "correct", "passed"]
            if any(kw in page_text.lower() for kw in success_keywords):
                print("SUCCESS!")
                await page.screenshot(path=str(project_dir / "success.png"))
                break

            # Failure indicators
            fail_keywords = ["error", "failed", "wrong", "incorrect"]
            if any(kw in page_text.lower() for kw in fail_keywords):
                print("FAILED")

                # Extract error text
                error_text = await page.inner_text("[class*='error'], [class*='fail'], [class*='message']").catch(lambda e: "")
                if error_text:
                    print(f"  Error: {error_text[:100]}")

                await page.screenshot(path=str(project_dir / f"error_{attempt}.png"))

                # Analyze error and fix
                print(f"\n[ANALYZING] Error screenshot saved: error_{attempt}.png")
                print("[WAITING FOR FIX] Waiting 30 seconds for code fix...")

                # Wait for potential code fix
                for i in range(30):
                    await page.wait_for_timeout(1000)

                    # Check if files were modified
                    try:
                        result = subprocess.run(['git', 'status', '--porcelain'],
                                              capture_output=True, text=True, cwd=str(project_dir))
                        if result.stdout.strip():
                            print("[DETECTED] Code changes found!")
                            break
                    except:
                        pass

                # Push any fixes
                print("[PUSHING] Pushing code changes...")
                push_code()
                print("[OK] Pushed")

                # Refresh for next attempt
                await page.reload(wait_until="networkidle")
                await page.wait_for_timeout(3000)
                print()

            else:
                print("UNCLEAR")
                await page.wait_for_timeout(2000)

        print("\n[DONE] Automation complete")
        print("[BROWSER] Keeping browser open for 30 seconds then closing...")

        # Keep browser open for review
        await page.wait_for_timeout(30000)  # 30 seconds

        await browser.close()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("HOLBERTON INTRANET AUTOMATION")
    print("="*60)
    print()

    asyncio.run(main())
