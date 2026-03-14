#!/usr/bin/env python3
import os
import sys
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def push_code():
    """Push code with commit message 'a'"""
    try:
        subprocess.run(['git', 'add', '-A'], check=True, capture_output=True, cwd=os.getcwd())
        result = subprocess.run(['git', 'commit', '-m', 'a'],
                              capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0 or "nothing to commit" in result.stdout:
            subprocess.run(['git', 'push'], capture_output=True, cwd=os.getcwd())
            print("[OK] Code pushed with message 'a'")
            return True
    except Exception as e:
        print(f"[ERROR] Push failed: {e}")
        return False

def run_automation():
    """Main automation - call this AFTER you're logged in"""

    os.chdir(r"C:\Users\Admin\Documents\projects\holbertonschool-cyber_security")

    # Setup driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Go to the project page
        url = "https://intranet.hbtn.io/projects/3118"
        print(f"[INFO] Navigating to {url}")
        driver.get(url)
        time.sleep(3)

        # Check if already logged in
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "project"))
            )
            print("[OK] Already logged in")
        except:
            print("[ACTION] You need to log in. Browser opened at the project page.")
            print("[INFO] Log in now, then press Enter here to continue:")
            input()

        # Push the code
        print("\n[STEP] Pushing code...")
        push_code()

        # Now run corrections in a loop
        correction_count = 0
        max_attempts = 10

        while correction_count < max_attempts:
            correction_count += 1
            print(f"\n[CORRECTION ATTEMPT {correction_count}/{max_attempts}]")

            # Refresh page
            driver.refresh()
            time.sleep(2)

            try:
                # Find and click the correction button
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'run the correction')]"))
                )
                print("[ACTION] Found 'run the correction' button, clicking...")
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(1)
                button.click()
                time.sleep(4)

                # Get page source to check for errors
                page_html = driver.page_source

                # Look for error messages
                if 'error' in page_html.lower() or 'failed' in page_html.lower():
                    print("[ERROR] Test failed - errors detected on page")

                    # Try to extract error message
                    try:
                        error_elem = driver.find_elements(By.CLASS_NAME, "error")
                        if error_elem:
                            for e in error_elem:
                                text = e.text
                                if text:
                                    print(f"  Error: {text}")
                    except:
                        pass

                    # Take screenshot for manual analysis
                    driver.save_screenshot(f"error_screenshot_{correction_count}.png")
                    print("[INFO] Screenshot saved: error_screenshot_{correction_count}.png")

                    print("\n[ACTION REQUIRED] Analyze the error:")
                    print("- Check the browser page for error details")
                    print("- Fix the code in the project folder")
                    print("- Save files and press Enter to continue (will push and retry)")
                    input()

                    # Push the fixes
                    push_code()

                elif 'success' in page_html.lower() or 'pass' in page_html.lower():
                    print("[OK] SUCCESS - All tests passed!")
                    break
                else:
                    # Status unclear, try again
                    print("[INFO] Status unclear, checking next iteration...")

            except Exception as e:
                print(f"[ERROR] {str(e)}")
                print("[ACTION] Browser window may have changed. Check it and press Enter to retry:")
                input()

        if correction_count >= max_attempts:
            print(f"\n[WARNING] Reached maximum attempts ({max_attempts})")

        print("\n[DONE] Automation complete!")
        print("[INFO] Browser will stay open. Press Enter to close it:")
        input()

    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("HOLBERTON INTRANET AUTOMATION")
    print("=" * 60)
    print("\n[IMPORTANT] Make sure you:")
    print("1. Have the intranet page open in this browser window")
    print("2. Are logged in to your account")
    print("3. Are on project page 3118")
    print("\n[INFO] Press Enter to start the automation:")
    input()

    run_automation()
