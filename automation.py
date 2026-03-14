#!/usr/bin/env python3
"""
Automates Holberton intranet project submission and correction.
Requires manual login first - script waits and continues after.
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("Selenium not available. Will use manual approach.")

def push_with_commit(message="a"):
    """Push code with given commit message."""
    try:
        subprocess.run(['git', 'add', '-A'], check=True, capture_output=True)
        result = subprocess.run(['git', 'commit', '-m', message],
                              capture_output=True, text=True)
        if result.returncode == 0:
            subprocess.run(['git', 'push'], check=True, capture_output=True)
            print(f"[OK] Pushed with commit '{message}'")
            return True
        elif "nothing to commit" in result.stdout:
            subprocess.run(['git', 'push'], capture_output=True)
            print(f"✓ No changes, pushed existing commits")
            return True
    except Exception as e:
        print(f"Push failed: {e}")
        return False

def wait_for_login():
    """Wait for user to complete login."""
    print("\n" + "="*60)
    print("WAITING FOR LOGIN")
    print("="*60)
    print("\n1. A Chrome window will open to the intranet")
    print("2. Sign in with your credentials")
    print("3. Return here and press Enter when logged in")
    print("\nPress Enter to continue...", end="", flush=True)
    input()

def run_with_selenium():
    """Run automation with Selenium."""
    project_url = "https://intranet.hbtn.io/projects/3118"
    project_dir = r"C:\Users\Admin\Documents\projects\holbertonschool-cyber_security"

    chrome_options = Options()
    # Keep window visible for login
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Navigate
        print(f"\nOpening {project_url}...")
        driver.get(project_url)

        # Wait for login
        wait_for_login()

        # Push code
        os.chdir(project_dir)
        push_with_commit("a")

        # Find and click "Run the correction" button
        max_attempts = 5
        attempt = 0

        while attempt < max_attempts:
            attempt += 1
            print(f"\n--- Correction Attempt {attempt}/{max_attempts} ---")

            # Refresh page
            driver.refresh()
            time.sleep(2)

            try:
                # Find correction button
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Run the correction')]"))
                )
                print("Found 'Run the correction' button, clicking...")
                driver.execute_script("arguments[0].scrollIntoView();", button)
                button.click()
                time.sleep(3)

                # Check for error messages
                page_html = driver.page_source

                if "error" in page_html.lower() and "failed" not in page_html.lower():
                    print("[ERROR] Error detected on page")

                    # Find error text
                    try:
                        error_elem = driver.find_element(By.CLASS_NAME, "error")
                        error_text = error_elem.text
                        print(f"Error message: {error_text}")

                        print("\nAnalyze and fix the error, then press Enter to try again...")
                        input()
                    except:
                        print("Could not extract error message")
                        print("Press Enter after fixing...")
                        input()

                elif "success" in page_html.lower() or "correct" in page_html.lower():
                    print("[OK] Task completed successfully!")
                    break
                else:
                    print("Status unclear. Checking next iteration...")
                    time.sleep(2)

            except Exception as e:
                print(f"Error: {e}")
                print("Press Enter to retry or exit...")
                user_input = input("(Press Enter to retry, or type 'exit' to quit): ")
                if user_input.lower() == 'exit':
                    break

    finally:
        print("\nPress Enter to close browser...")
        input()
        driver.quit()

def main():
    print("\n" + "="*60)
    print("HOLBERTON INTRANET PROJECT AUTOMATION")
    print("="*60)

    if not SELENIUM_AVAILABLE:
        print("\n[WARNING] Selenium not installed. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'selenium'],
                      capture_output=True)
        print("[OK] Selenium installed")

    os.chdir(r"C:\Users\Admin\Documents\projects\holbertonschool-cyber_security")

    try:
        run_with_selenium()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
