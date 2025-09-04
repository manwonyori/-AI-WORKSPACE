#!/usr/bin/env python3
"""
Puppeteer를 사용한 실제 AI 플랫폼 셀렉터 검증 도구
MCP Puppeteer 서버를 통해 실제 웹사이트의 DOM 구조를 확인합니다.
"""

import json
import asyncio
import subprocess
from datetime import datetime

class AIPageTester:
    def __init__(self):
        self.platforms = {
            'chatgpt': 'https://chatgpt.com',
            'claude': 'https://claude.ai',
            'perplexity': 'https://perplexity.ai',
            'gemini': 'https://gemini.google.com'
        }
        
        self.selectors = {
            'chatgpt': {
                'input': [
                    'div[contenteditable="true"][data-id="root"]',
                    'div[contenteditable="true"][data-placeholder*="Message"]',
                    'div[contenteditable="true"][aria-label*="Message"]',
                    'div.m-0.w-full.resize-none[contenteditable="true"]'
                ],
                'button': [
                    'button[data-testid="send-button"]',
                    'button[aria-label*="Send"]',
                    'button[type="submit"]'
                ]
            },
            'claude': {
                'input': [
                    'div[contenteditable="true"].ProseMirror',
                    'div[contenteditable="true"][data-placeholder]',
                    'div[role="textbox"][contenteditable="true"]'
                ],
                'button': [
                    'button[aria-label="Send Message"]',
                    'button[data-testid="send-button"]'
                ]
            },
            'perplexity': {
                'input': [
                    'textarea.SearchBar-input[data-testid="search-bar-input"]',
                    'textarea.SearchBar-input',
                    'textarea[data-testid="search-bar-input"]',
                    'textarea[aria-label*="Ask anything"]'
                ],
                'button': [
                    'button.SearchBar-sendButton[data-testid="send-btn"]',
                    'button.SearchBar-sendButton',
                    'button[data-testid="send-btn"]'
                ]
            },
            'gemini': {
                'input': [
                    'rich-textarea textarea',
                    'textarea[aria-label*="Enter a prompt"]',
                    'textarea[aria-label*="Type something"]',
                    'textarea[data-test-id="text-input"]'
                ],
                'button': [
                    'button[aria-label*="Send"]',
                    'button[aria-label*="Run"]',
                    'button[data-test-id="send-button"]'
                ]
            }
        }
    
    async def test_platform(self, platform_name):
        """특정 플랫폼의 셀렉터를 테스트합니다."""
        url = self.platforms.get(platform_name)
        if not url:
            return None
        
        print(f"\nTesting {platform_name.upper()} at {url}")
        print("-" * 50)
        
        # Puppeteer 스크립트 생성
        script = f"""
const puppeteer = require('puppeteer');

(async () => {{
    const browser = await puppeteer.launch({{
        headless: false,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }});
    
    const page = await browser.newPage();
    await page.goto('{url}', {{ waitUntil: 'networkidle2', timeout: 30000 }});
    
    // Wait for page to load
    await page.waitForTimeout(3000);
    
    // Test input selectors
    const inputSelectors = {json.dumps(self.selectors[platform_name]['input'])};
    let inputFound = null;
    
    for (const selector of inputSelectors) {{
        try {{
            const element = await page.$(selector);
            if (element) {{
                console.log(`[OK] Input found: ${{selector}}`);
                inputFound = selector;
                
                // Get element attributes
                const attrs = await page.evaluate(el => {{
                    const attributes = {{}};
                    for (const attr of el.attributes) {{
                        attributes[attr.name] = attr.value;
                    }}
                    return {{
                        tagName: el.tagName.toLowerCase(),
                        className: el.className,
                        id: el.id,
                        attributes: attributes
                    }};
                }}, element);
                
                console.log('Element details:', JSON.stringify(attrs, null, 2));
                break;
            }}
        }} catch (e) {{
            console.log(`[ERROR] Error with selector: ${{selector}}`);
        }}
    }}
    
    if (!inputFound) {{
        console.log('[ERROR] No input element found');
    }}
    
    // Test button selectors
    const buttonSelectors = {json.dumps(self.selectors[platform_name]['button'])};
    let buttonFound = null;
    
    for (const selector of buttonSelectors) {{
        try {{
            const element = await page.$(selector);
            if (element) {{
                console.log(`[OK] Button found: ${{selector}}`);
                buttonFound = selector;
                break;
            }}
        }} catch (e) {{
            console.log(`[ERROR] Error with selector: ${{selector}}`);
        }}
    }}
    
    if (!buttonFound) {{
        console.log('[ERROR] No button element found');
    }}
    
    // Take screenshot
    await page.screenshot({{ path: '{platform_name}_test.png', fullPage: false }});
    console.log(`[SCREENSHOT] Saved: {platform_name}_test.png`);
    
    await browser.close();
}})();
        """
        
        # Save and run the script
        script_file = f"test_{platform_name}.js"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script)
        
        try:
            # Run the puppeteer script
            result = subprocess.run(
                ['node', script_file],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            print("Output:")
            print(result.stdout)
            if result.stderr:
                print("Errors:")
                print(result.stderr)
                
            return {
                'platform': platform_name,
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
        except subprocess.TimeoutExpired:
            print(f"[ERROR] Timeout while testing {platform_name}")
            return None
        except Exception as e:
            print(f"[ERROR] Error testing {platform_name}: {e}")
            return None
    
    async def test_all(self):
        """모든 플랫폼을 테스트합니다."""
        results = {}
        for platform in self.platforms.keys():
            result = await self.test_platform(platform)
            if result:
                results[platform] = result
        
        # Save results
        with open('platform_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 50)
        print("Test Results Summary")
        print("=" * 50)
        for platform, result in results.items():
            if result:
                has_input = "OK" if "Input found" in result['stdout'] else "FAIL"
                has_button = "OK" if "Button found" in result['stdout'] else "FAIL"
                print(f"{platform.upper():12} Input: {has_input}  Button: {has_button}")
        
        print(f"\n[SAVED] Full results saved to: platform_test_results.json")
        return results

if __name__ == "__main__":
    tester = AIPageTester()
    
    print("AI Platform Selector Tester")
    print("=" * 50)
    print("1. Test all platforms")
    print("2. Test ChatGPT only")
    print("3. Test Claude only")
    print("4. Test Perplexity only")
    print("5. Test Gemini only")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        asyncio.run(tester.test_all())
    elif choice == "2":
        asyncio.run(tester.test_platform('chatgpt'))
    elif choice == "3":
        asyncio.run(tester.test_platform('claude'))
    elif choice == "4":
        asyncio.run(tester.test_platform('perplexity'))
    elif choice == "5":
        asyncio.run(tester.test_platform('gemini'))
    else:
        print("Invalid option")