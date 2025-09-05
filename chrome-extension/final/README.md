# AI Ultimate Auto-Relay Chrome Extension

## Installation

1. Open Chrome browser
2. Go to `chrome://extensions/`
3. Enable **Developer mode** (toggle switch in top-right corner)
4. Click **Load unpacked** button
5. Select this folder: `C:\Users\8899y\AI-WORKSPACE\chrome-extension\final`
6. The extension icon will appear in your toolbar

## Features

- **Multi-AI Support**: Works with ChatGPT, Claude, Gemini, and Perplexity
- **Broadcast Messages**: Send the same message to all AI platforms simultaneously
- **Auto-Relay**: Automatically relay responses between AIs for collaborative work
- **Real-time Monitoring**: Track all activities and responses
- **Premium UI**: Beautiful gradient design with intuitive controls

## How to Use

### Basic Usage
1. Click the extension icon in Chrome toolbar
2. Click **"모든 탭 열기"** to open all AI platforms
3. Wait for all platforms to load (indicators will turn green)
4. Type your message in the text box
5. Click **"전체 전송"** to send to all AIs

### Auto-Relay Mode
1. Enter your project objective in the relay text box
2. Click **"시작"** to start automatic relay
3. The AIs will collaborate automatically
4. Click **"중지"** to stop the relay

### Monitoring
- Click **"표시"** to see real-time logs
- Check statistics for success/fail counts
- Click **"모니터 열기"** for detailed dashboard

## File Structure

```
final/
├── manifest.json      # Extension configuration
├── background.js      # Service worker (handles relay logic)
├── content.js         # Content script (interacts with AI sites)
├── popup.html         # Main UI
├── popup.js           # Popup controller
├── monitor.html       # Monitoring dashboard
└── icon.png           # Extension icon
```

## Troubleshooting

- **Platform not responding**: Refresh the AI platform tab and try again
- **Message not sending**: Make sure you're logged into all AI platforms
- **Extension not loading**: Check that all files are present in the folder

## Version

v3.0.0 - ULTIMATE Edition

---

Ready to use! Click the extension icon to get started.