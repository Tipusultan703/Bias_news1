function highlightChanges(data) {
    if (!data.redlined_text || typeof data.redlined_text !== "string") {
        console.warn("⚠️ No valid redlined_text received.");
        return;
    }

    console.log("🔍 Applying Text Modifications...");
    
    let originalText = data.original.trim();
    let modifiedText = data.redlined_text.trim();

    // Only update elements containing the original text
    document.querySelectorAll("*").forEach((element) => {
        if (element.children.length === 0 && element.textContent.includes(originalText)) {
            element.innerHTML = element.innerHTML.replace(
                originalText,
                modifiedText
                    .replace(/~~(.*?)~~/g, `<span style="text-decoration: line-through; color: red;">$1</span>`)  // Removed words
                    .replace(/\+\+(.*?)\+\+/g, `<span style="text-decoration: underline; color: green;">$1</span>`)  // Added words
            );
        }
    });

    console.log("✅ Highlighting Complete");
}

