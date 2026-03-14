function startAutomation() {
  const status = document.getElementById('status');
  status.className = 'info';
  status.textContent = 'Starting automation...';

  chrome.runtime.sendMessage({ action: 'start' }, (response) => {
    if (response && response.success) {
      status.className = 'success';
      status.textContent = 'Automation started!';
    } else {
      status.className = 'error';
      status.textContent = 'Error starting automation';
    }
  });
}

function stopAutomation() {
  const status = document.getElementById('status');
  status.className = 'info';
  status.textContent = 'Stopping automation...';

  chrome.runtime.sendMessage({ action: 'stop' }, (response) => {
    if (response && response.success) {
      status.className = 'success';
      status.textContent = 'Automation stopped';
    }
  });
}

// Check status on load
window.addEventListener('load', () => {
  chrome.runtime.sendMessage({ action: 'getStatus' }, (response) => {
    const status = document.getElementById('status');
    if (response) {
      status.textContent = response.status;
      if (response.isRunning) {
        status.className = 'info';
      }
    }
  });
});
