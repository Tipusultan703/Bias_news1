document.addEventListener("DOMContentLoaded", function () {
    let analyzeButton = document.getElementById("analyzeButton");
    let resultDiv = document.getElementById("result");

    if (analyzeButton) {
        analyzeButton.addEventListener("click", () => {
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                chrome.tabs.sendMessage(tabs[0].id, { action: "analyze" });
            });
        });
    }

    // Load previous results
    chrome.storage.local.get(["analysis"], (result) => {
        if (result.analysis) {
            let data = result.analysis;
            resultDiv.innerHTML = `
                <h3>Bias Score: ${data.bias_score}</h3>
                <p><strong>Rewritten:</strong> ${data.rewritten}</p>
                <p><strong>Sources:</strong> ${data.sources.join(", ")}</p>
                <p><strong>Redlined Text:</strong> ${data.redlined_text.join("<br>")}</p>
            `;
        }
    });
});



