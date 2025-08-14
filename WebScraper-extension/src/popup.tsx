import { useEffect, useState } from "react";

export default function Popup() {
  const [time, setTime] = useState(0);
  const [last, setLast] = useState<string>("(no selection yet)");

  useEffect(() => {
    const timer = setInterval(() => setTime((t) => t + 1), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    // Guard for non-extension environments
    const hasChrome = typeof chrome !== "undefined" && !!chrome.storage;

    if (hasChrome) {
      chrome.storage.local.get("lastSelection", (data) => {
        if (data?.lastSelection) setLast(data.lastSelection as string);
      });

      // Optional: listen for changes
      chrome.storage.onChanged.addListener((changes, area) => {
        if (area === "local" && changes.lastSelection) {
          setLast(changes.lastSelection.newValue || "");
        }
      });
    }
  }, []);

  return (
    <div style={{ padding: 12, width: 280, fontFamily: "system-ui, sans-serif" }}>
      <h2 style={{ margin: "0 0 8px" }}>Web Scraper</h2>
      <p style={{ margin: "0 0 8px" }}>Toolbar popup is working 🎉</p>
      <p style={{ margin: "0 0 6px", fontSize: 12, opacity: 0.8 }}>
        Uptime: {time}s
      </p>
      <div style={{
        padding: "8px 10px",
        background: "#f5f5f7",
        borderRadius: 8,
        minHeight: 50,
        whiteSpace: "pre-wrap",
        wordBreak: "break-word"
      }}>
        {last}
      </div>
    </div>
  );
}
