document.addEventListener("mouseup", () => {
  const selection = window.getSelection();
  const text = selection ? selection.toString().trim() : "";

  if (text) {
    const range = selection.getRangeAt(0); // The selected text's range
    const rect = range.getBoundingClientRect(); // Position in the viewport

    const x = rect.left + window.scrollX;
    const y = rect.top + window.scrollY;

    console.log("Selected text:", text);
    console.log("Position:", { x, y });

    // Example: Create popup
    showPopup(x, y, text);
  }
});

function showPopup(x, y, text) {
  let popup = document.createElement("div");
  popup.className = "sayanExtension"
  popup.innerText = `Translate: ${text}`;
  popup.style.position = "absolute";
  popup.style.left = `${x}px`;
  popup.style.top = `${y - 40}px`; // above the selection
  popup.style.background = "#fff";
  popup.style.border = "1px solid #ccc";
  popup.style.padding = "5px 10px";
  popup.style.borderRadius = "5px";
  popup.style.boxShadow = "0 2px 6px rgba(0,0,0,0.2)";
  popup.style.zIndex = 999999;

  document.body.appendChild(popup);

  // Remove old popup after a few seconds
  setTimeout(() => popup.remove(), 3000);
  const sayanExtension = document.querySelector(".sayanExtension");
  document.addEventListener('click',()=>{
    if(!sayanExtension.addEventListener("click")){
        console.log("it is out side ");
    }
  })
}


// code for selected text

document.addEventListener("selectionchange",()=>{
    const selection = window.getSelection();
    const text = selection ? selection.toString().trim() : "";
    if (text){

    }
})
console.log("it is injected ");