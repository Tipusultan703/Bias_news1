chrome.runtime.onInstalled.addListener(() => {
    console.log("Bias-Free News Extension Installed ✅");

    // Set default bias threshold
    chrome.storage.local.set({ biasThreshold: 50 }, () => {
        console.log("Default Bias Threshold set to 50");
    });
});

// Function to retrieve stored settings
function getBiasThreshold(callback) {
    chrome.storage.local.get(["biasThreshold"], (result) => {
        console.log("Stored Bias Threshold:", result.biasThreshold);
        callback(result.biasThreshold || 50);
    });
}

// Listen for messages from popup or content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "getBiasThreshold") {
        getBiasThreshold(sendResponse);
        return true; // Required for async response
    }
});

