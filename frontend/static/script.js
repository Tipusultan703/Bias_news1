let biasChartInstance = null;  // Store chart instance
let firstCheckDone = false;  // Ensure checkScore runs only once
let isOriginalVisible = true;  // Track toggle state

function analyzeNews() {
    let text = document.getElementById("newsText").value.trim();
    if (!text) return alert("Please enter news text.");

    fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
    })
    .then(response => {
        if (!response.ok) throw new Error(`Server Error: ${response.status}`);
        return response.json();
    })
    .then(data => {
        if (!data.redlined_text || !Array.isArray(data.redlined_text)) {
            data.redlined_text = ["No biased terms found."];  // ✅ Ensure it's a list
        }

        document.getElementById("biasScore").innerText = `Bias Score: ${data.bias_score}`;
        document.getElementById("originalText").innerText = text;
        document.getElementById("rewrittenText").innerText = data.rewritten;
        document.getElementById("sources").innerText = `Sources: ${data.sources.join(", ")}`;

        // ✅ Fix `.map()` issue
        let redlinedHtml = data.redlined_text.map(change => {
            if (change.includes("❌ Removed:")) {
                return `<span style="color: red;">${change}</span>`;
            } else if (change.includes("✅ Added:")) {
                return `<span style="color: green;">${change}</span>`;
            }
            return change;
        }).join("<br>");

        document.getElementById("redlinedText").innerHTML = redlinedHtml;
        document.getElementById("result").style.display = "block";

        // ✅ Update Bias Score Chart
        updateBiasChart(data.bias_score);
    })
    .catch(error => {
        console.error("Error analyzing news:", error);
        alert(`Failed to analyze text. ${error.message}`);
    });
}


// ✅ Check Source (Works First Time Only)
function checkSource() {
    if (firstCheckDone) {
        alert("⚠️ You have already checked a source. Refresh to check again.");
        return;
    }

    let url = document.getElementById("newsUrl").value.trim();
    if (!url) {
        alert("❌ Please enter a URL.");
        return;
    }

    fetch("http://127.0.0.1:5000/source_check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        document.getElementById("sourceBiasScore").innerText = `Bias Score: ${data.bias_score}`;
        document.getElementById("source-result").style.display = "block";
        firstCheckDone = true;
    })
    .catch(error => {
        console.error("❌ Error checking source:", error);
        alert("Failed to check source. Please try again.");
    });
}

function updateBiasChart(newScore) {
    let ctx = document.getElementById("biasChart").getContext("2d");

    if (biasChartInstance) {
        biasChartInstance.destroy();
    }

    biasChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Bias Score"],
            datasets: [{
                label: "Bias Score",
                data: [newScore],
                backgroundColor: "blue",
            }]
        }
    });
}

// Toggle View 
function toggleView() {
    isOriginalVisible = !isOriginalVisible;
    document.getElementById("originalText").style.display = isOriginalVisible ? "block" : "none";
    document.getElementById("rewrittenText").style.display = isOriginalVisible ? "none" : "block";
}

//  Flag Article as Incorrect
function flagArticle() {
    let text = document.getElementById("originalText").innerText;
    if (!text) {
        alert("❌ No article to flag.");
        return;
    }

    fetch("http://127.0.0.1:5000/flag", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ flagged_text: text })
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        alert(data.message || "✅ Article flagged successfully!");
    })
    .catch(error => {
        console.error("❌ Error flagging article:", error);
        alert("Failed to flag article. Please try again.");
    });
}







