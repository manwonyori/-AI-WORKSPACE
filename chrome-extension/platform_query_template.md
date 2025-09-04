# AI 플랫폼별 입력/전송 구조 질문 템플릿

## ChatGPT에게 물어볼 질문:

```
I'm developing a Chrome extension that needs to programmatically input text and send messages in ChatGPT. 

Current issue: After setting text in the textarea, the send button (with arrow SVG path "M8.99992 16V6.41407...") appears but clicking it programmatically doesn't always work.

My current approach:
1. Find textarea with selector: #prompt-textarea
2. Set value using React's native setter:
   ```javascript
   const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
   setter.call(textarea, text);
   textarea.dispatchEvent(new Event('input', { bubbles: true }));
   ```
3. Wait for send button to appear
4. Click the button

Questions:
1. What's the correct way to programmatically set text in ChatGPT's input?
2. What events should I dispatch after setting the text?
3. How can I reliably trigger the send button after text input?
4. Are there any specific React event handlers I should trigger?

Can you provide the exact JavaScript code that would work reliably?
```

## Gemini/AI Studio에게 물어볼 질문:

```
I'm developing a Chrome extension for Google AI Studio/Gemini that needs to programmatically input text and send messages.

Current issue: The interface uses a Quill editor (div.ql-editor) and after inputting text, a mat-icon send button appears, but programmatic clicking doesn't always work.

My current approach:
1. Find the Quill editor: div.ql-editor
2. Set content:
   ```javascript
   editor.innerHTML = `<p>${text}</p>`;
   editor.dispatchEvent(new Event('input', { bubbles: true }));
   ```
3. Wait for mat-icon[fonticon="send"] to appear
4. Click the button or mat-icon

Questions:
1. What's the proper way to programmatically input text in the Quill editor?
2. Should I use Quill's API directly, or DOM manipulation?
3. How do I properly trigger the send action after input?
4. What's the relationship between the mat-icon and its parent button?
5. Are there Angular-specific events I should dispatch?

Can you provide working JavaScript code for reliable text input and sending?
```

## Claude에게 물어볼 질문:

```
I'm developing a Chrome extension that interacts with AI chat interfaces. For your interface (Claude), I need to programmatically:
1. Input text into the message field
2. Send the message

Currently I'm using:
- Selector: div[contenteditable="true"].ProseMirror
- Method: Set textContent and dispatch InputEvent

This works well for Claude. But I'm having issues with ChatGPT and Gemini where buttons appear dynamically after text input.

Can you help me understand:
1. The general patterns for React-based inputs (like ChatGPT)
2. The patterns for Angular Material inputs (like Gemini)
3. How to properly wait for and trigger dynamically appearing buttons
4. Best practices for simulating user input in modern web apps

Specifically, I need help with:
- ChatGPT: Button with SVG path "M8.99992 16V6.41407..." that appears after input
- Gemini: mat-icon[fonticon="send"] button that appears after Quill editor input
```

## Perplexity에게 물어볼 질문:

```
I need to programmatically interact with AI chat interfaces via Chrome extension. Can you provide working code examples for:

1. **ChatGPT (React-based)**:
   - Input selector: textarea#prompt-textarea
   - Send button: Contains SVG path "M8.99992 16V6.41407..."
   - Issue: Button appears only after text input, clicking doesn't always work

2. **Google AI Studio/Gemini (Angular Material)**:
   - Input: div.ql-editor (Quill editor)  
   - Send button: mat-icon[fonticon="send"]
   - Issue: Button appears dynamically, click events don't trigger send

Please provide:
- Exact JavaScript code for text input
- Proper event dispatching sequences
- Methods to wait for and click dynamic buttons
- Framework-specific considerations (React vs Angular)

Current working example (Claude):
```javascript
const input = document.querySelector('div[contenteditable="true"]');
input.textContent = text;
input.dispatchEvent(new InputEvent('input', { bubbles: true }));
```

Need similar reliable solutions for ChatGPT and Gemini.
```

## 각 플랫폼에서 테스트할 디버그 코드:

```javascript
// 현재 페이지의 입력/전송 구조를 분석하는 코드
console.log("=== Input/Send Structure Analysis ===");

// Find input elements
const inputs = document.querySelectorAll('textarea, [contenteditable="true"], .ql-editor');
console.log(`Found ${inputs.length} input elements:`);
inputs.forEach((el, i) => {
  console.log(`${i+1}. ${el.tagName}.${el.className} #${el.id}`);
});

// Find buttons
const buttons = document.querySelectorAll('button, [role="button"], mat-icon');
console.log(`\nFound ${buttons.length} button elements`);

// Monitor for new buttons
const observer = new MutationObserver((mutations) => {
  mutations.forEach(mutation => {
    mutation.addedNodes.forEach(node => {
      if (node.nodeName === 'BUTTON' || 
          (node.querySelector && node.querySelector('button, mat-icon'))) {
        console.log('New button appeared:', node);
      }
    });
  });
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});

console.log("\nMutation observer started. Type something to see what appears...");
```