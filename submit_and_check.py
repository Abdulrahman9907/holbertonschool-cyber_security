#!/usr/bin/env python3
"""
Simple script that opens the intranet, waits for you to login,
then helps automate pushing and running corrections.
"""

import os
import sys
import time
import webbrowser

def main():
    project_url = "https://intranet.hbtn.io/projects/3118"
    project_dir = r"C:\Users\Admin\Documents\projects\holbertonschool-cyber_security"

    print("=" * 60)
    print("HOLBERTON INTRANET PROJECT SUBMISSION")
    print("=" * 60)

    print(f"\n[STEP 1] Opening intranet project page...")
    print(f"URL: {project_url}")
    print("\n[ACTION] Opening browser now. Please login to your intranet account.")

    # Open browser
    webbrowser.open(project_url)

    print("\nWaiting for your login... Press Enter when you're logged in and ready:")
    input()

    print("\n[STEP 2] Next steps:")
    print("1. I'll push the code with commit message 'a'")
    print("2. Then we'll click 'Run the correction' on the intranet")
    print("3. If there are errors, we'll fix them")
    print("4. Repeat until all tests pass")

    print("\nPress Enter to continue with the push and correction process:")
    input()

    os.chdir(project_dir)

    print("\n[STEP 3] Pushing code with message 'a'...")

    import subprocess

    # Add all files
    result = subprocess.run(['git', 'add', '-A'], capture_output=True, text=True)
    print(f"  git add -A: {result.returncode}")

    # Commit with message 'a'
    result = subprocess.run(['git', 'commit', '-m', 'a'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  git commit -m 'a': Success")
    elif "nothing to commit" in result.stdout:
        print(f"  git commit: (nothing to commit - already up to date)")
    else:
        print(f"  git commit: {result.stderr}")

    # Push
    result = subprocess.run(['git', 'push'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  git push: Success")
    else:
        print(f"  git push: {result.stderr[:100]}")

    print("\n[STEP 4] Code has been pushed!")
    print("\nNow on the intranet page:")
    print("1. Look for a 'Run the correction' or 'Run tests' button")
    print("2. Click it to run the automated checks")
    print("3. If you see errors, analyze them and fix the code")
    print("4. Repeat until all checks pass")

    print("\nManual process from here - switch to your browser window.")
    print("This script has done what it can automatically.")

if __name__ == "__main__":
    main()
