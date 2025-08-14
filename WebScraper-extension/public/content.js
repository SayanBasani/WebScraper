let popupDiv = null;

document.addEventListener("mouseup", () => {
    const selection = window.getSelection();
    const selectedText = selection ? selection.toString().trim() : "";

    // Remove old popup if exists
    if (popupDiv) {
        popupDiv.remove();
        popupDiv = null;
    }

    if (selectedText.length > 0) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        // Create popup
        popupDiv = document.createElement("div");
        popupDiv.className = "custom-translate-popup";
        popupDiv.innerHTML = `
            <div class="popup-arrow"></div>
            <div class="popup-content">${selectedText}</div>
        `;

        document.body.appendChild(popupDiv);

        // Position popup
        popupDiv.style.top = `${window.scrollY + rect.top - popupDiv.offsetHeight - 10}px`;
        popupDiv.style.left = `${window.scrollX + rect.left + rect.width / 2 - popupDiv.offsetWidth / 2}px`;

        // Action on click
        popupDiv.addEventListener("click", () => {
            alert("You clicked: " + selectedText);
            // You can send this to your API instead of alert
        });
    }
});

document.addEventListener("mousedown", (event) => {
    // Remove popup if clicked outside
    if (popupDiv && !popupDiv.contains(event.target)) {
        popupDiv.remove();
        popupDiv = null;
    }
});
