let automationRunning = false;
let currentAttempt = 0;
const MAX_ATTEMPTS = 10;

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'start') {
    automationRunning = true;
    currentAttempt = 0;
    sendResponse({ success: true });
    runAutomation();
  } else if (request.action === 'stop') {
    automationRunning = false;
    sendResponse({ success: true });
  } else if (request.action === 'getStatus') {
    sendResponse({
      isRunning: automationRunning,
      status: automationRunning ? `Running (attempt ${currentAttempt}/${MAX_ATTEMPTS})` : 'Idle',
    });
  }
});

async function runAutomation() {
  console.log('[AUTO] Starting automation...');

  // First: trigger git push via Python backend
  await triggerGitPush();

  // Second: run correction loop
  while (automationRunning && currentAttempt < MAX_ATTEMPTS) {
    currentAttempt++;
    console.log(`[AUTO] Correction attempt ${currentAttempt}/${MAX_ATTEMPTS}`);

    // Find and click correction button
    const button = findCorrectionButton();
    if (!button) {
      console.log('[AUTO] No correction button found');
      break;
    }

    // Click button
    button.click();
    await sleep(6000);

    // Check results
    const pageText = document.body.innerText.toLowerCase();

    if (pageText.includes('success') || pageText.includes('passed') || pageText.includes('all test')) {
      console.log('[AUTO] SUCCESS - All tests passed!');
      automationRunning = false;
      break;
    } else if (pageText.includes('error') || pageText.includes('failed')) {
      console.log('[AUTO] FAILED - Waiting for code fix...');
      // Wait for code fix (30 seconds)
      await sleep(30000);
      // Git push happens again
      await triggerGitPush();
      // Refresh page
      location.reload();
      await sleep(3000);
    } else {
      console.log('[AUTO] Status unclear, retrying...');
      await sleep(2000);
    }
  }

  console.log('[AUTO] Automation completed');
  automationRunning = false;
}

function findCorrectionButton() {
  const buttons = document.querySelectorAll('button');
  for (const btn of buttons) {
    if (btn.textContent.toLowerCase().includes('correction')) {
      return btn;
    }
  }
  return null;
}

async function triggerGitPush() {
  // Send request to local Python server
  try {
    const response = await fetch('http://localhost:9999/git-push', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    const data = await response.json();
    console.log('[GIT]', data.message);
  } catch (e) {
    console.log('[GIT] Could not reach git server:', e.message);
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
