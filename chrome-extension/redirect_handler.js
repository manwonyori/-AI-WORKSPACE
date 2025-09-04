// Google AI Studio URL Redirect Handler
// This script handles the 500 error redirect issue

console.log("🔄 Google AI Studio Redirect Handler");

// Check current URL
const currentUrl = location.href;
console.log("Current URL:", currentUrl);

// If we're on the 500 page, redirect to the proper chat page
if (currentUrl.includes("aistudio.google.com/500") || 
    currentUrl.includes("aistudio.google.com/app") ||
    currentUrl === "https://aistudio.google.com/" ||
    currentUrl.includes("aistudio.google.com/chat")) {
    
    console.log("⚠️ Detected problematic URL, redirecting to proper chat page...");
    
    // Small delay to avoid redirect loops
    setTimeout(() => {
        console.log("🔄 Redirecting to: https://aistudio.google.com/prompts/new_chat");
        window.location.href = "https://aistudio.google.com/prompts/new_chat";
    }, 1000);
}

// Also check for proper URL pattern
if (currentUrl.includes("aistudio.google.com/prompts/")) {
    console.log("✅ Already on proper AI Studio URL");
} else if (currentUrl.includes("aistudio.google.com")) {
    console.log("⚠️ On AI Studio but not on prompts page");
}