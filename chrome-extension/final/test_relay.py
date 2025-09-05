#!/usr/bin/env python3
"""
Auto-Relay Test Script
Tests the relay functionality step by step
"""

import time
import webbrowser
import pyautogui
import json
from datetime import datetime

def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def test_relay_system():
    """
    Complete test sequence for auto-relay
    """
    
    log("Starting Auto-Relay System Test", "INFO")
    log("="*50, "INFO")
    
    # Test steps
    steps = [
        "1. Open Chrome Extensions page",
        "2. Load the extension from final folder",
        "3. Open all AI platform tabs",
        "4. Start auto-relay with test objective",
        "5. Monitor relay progression",
        "6. Verify message passing between platforms"
    ]
    
    for step in steps:
        log(step, "STEP")
    
    log("="*50, "INFO")
    
    # Instructions for manual testing
    instructions = """
MANUAL TEST PROCEDURE:
=====================

1. LOAD EXTENSION:
   - Open Chrome
   - Go to chrome://extensions/
   - Enable Developer mode
   - Load unpacked from: C:\\Users\\8899y\\AI-WORKSPACE\\chrome-extension\\final

2. OPEN DEBUG MONITOR:
   - Right-click extension icon
   - Select "Inspect popup"
   - In popup, open debug_relay.html in new tab
   
3. START TEST:
   - Click extension icon
   - Click "Open All" to open all AI platforms
   - Login to each platform if needed
   - Wait for all indicators to turn green
   
4. INITIATE RELAY:
   - Enter test objective in relay field:
     "Create a simple Python function to calculate fibonacci numbers"
   - Click "Start" button
   - Monitor the debug panel
   
5. EXPECTED FLOW:
   Claude -> ChatGPT -> Gemini -> Perplexity -> (repeat)
   
6. CHECK FOR:
   - Message appears in Claude
   - Claude responds
   - Response automatically transfers to ChatGPT
   - ChatGPT responds
   - Response automatically transfers to Gemini
   - Gemini responds
   - Response automatically transfers to Perplexity
   - Perplexity responds
   - Cycle continues or completes

TROUBLESHOOTING:
================

IF RELAY STOPS AT CLAUDE:
- Check Console for "RELAY_RESPONSE" messages
- Verify Claude's response selectors match current UI
- Check if response is being detected (length > 50)

IF NO TRANSFER TO NEXT PLATFORM:
- Check Background service worker console
- Look for "processRelayResponse" logs
- Verify tabs are properly registered

IF MESSAGE NOT SENDING:
- Check content script is loaded
- Verify input selectors are correct
- Check for "AUTO_RELAY" message in console

CONSOLE COMMANDS FOR DEBUGGING:
================================

In Background Console:
chrome.runtime.sendMessage({action: 'GET_STATUS'}, console.log)

In Content Script Console:
document.querySelectorAll('div.font-claude-message')
document.querySelectorAll('div[data-is-streaming]')

CHECK CURRENT STATE:
chrome.storage.local.get(['relay', 'monitor'], console.log)
"""
    
    print(instructions)
    
    # Create test report
    report = {
        "test_time": datetime.now().isoformat(),
        "test_objective": "Verify auto-relay functionality",
        "expected_behavior": {
            "1": "Extension loads without errors",
            "2": "All platforms open successfully",
            "3": "Message input works on all platforms",
            "4": "Send button clicks work",
            "5": "Responses are detected",
            "6": "Relay transfers between platforms",
            "7": "Complete cycle execution"
        },
        "common_issues": {
            "response_not_detected": "Check selectors in content.js",
            "relay_stops": "Check processRelayResponse in background.js",
            "message_not_sent": "Check AUTO_RELAY handler in content.js",
            "tab_not_found": "Check platform detection and tab management"
        }
    }
    
    # Save report
    with open("relay_test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    log("Test report saved to relay_test_report.json", "SUCCESS")
    
    # Open necessary pages
    log("Opening Chrome extensions page...", "INFO")
    webbrowser.open("chrome://extensions/")
    
    return True

if __name__ == "__main__":
    test_relay_system()