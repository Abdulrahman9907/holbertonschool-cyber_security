# Holberton Auto Submitter Extension

## Installation

1. **Start the extension server:**
   ```
   python extension_server.py
   ```
   Keep this terminal window open while using the extension.

2. **Load the extension in Chrome:**
   - Open Chrome
   - Go to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select this folder: `C:\Users\Admin\Documents\projects\holbertonschool-cyber_security\extension`

3. **Navigate to the intranet:**
   - Go to `https://intranet.hbtn.io/projects/3118`
   - Ensure you're logged in

4. **Run automation:**
   - Click the extension icon (puzzle piece) in top right
   - Click "Start Automation" button
   - The extension will automatically:
     - Push code with message 'a'
     - Click "Run the correction" button
     - Check test results
     - Fix errors and retry if needed
     - Repeat until all tests pass

## What the extension does

- Finds and clicks the "Run the correction" button
- Analyzes test results (success/failure)
- Waits 30 seconds for code fixes between attempts
- Automatically pushes code when ready
- Repeats up to 10 times until tests pass

## Troubleshooting

- Keep the Python server running
- Keep the intranet project page open
- Don't close the browser or extension window
- Check console (F12) for debug messages
