import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
export default function Popup() {
    const [time, setTime] = useState(0);
    const [last, setLast] = useState("(no selection yet)");
    useEffect(() => {
        const timer = setInterval(() => setTime((t) => t + 1), 1000);
        return () => clearInterval(timer);
    }, []);
    useEffect(() => {
        // Guard for non-extension environments
        const hasChrome = typeof chrome !== "undefined" && !!chrome.storage;
        if (hasChrome) {
            chrome.storage.local.get("lastSelection", (data) => {
                if (data?.lastSelection)
                    setLast(data.lastSelection);
            });
            // Optional: listen for changes
            chrome.storage.onChanged.addListener((changes, area) => {
                if (area === "local" && changes.lastSelection) {
                    setLast(changes.lastSelection.newValue || "");
                }
            });
        }
    }, []);
    return (_jsxs("div", { style: { padding: 12, width: 280, fontFamily: "system-ui, sans-serif" }, children: [_jsx("h2", { style: { margin: "0 0 8px" }, children: "Web Scraper" }), _jsx("p", { style: { margin: "0 0 8px" }, children: "Toolbar popup is working \uD83C\uDF89" }), _jsxs("p", { style: { margin: "0 0 6px", fontSize: 12, opacity: 0.8 }, children: ["Uptime: ", time, "s"] }), _jsx("div", { style: {
                    padding: "8px 10px",
                    background: "#f5f5f7",
                    borderRadius: 8,
                    minHeight: 50,
                    whiteSpace: "pre-wrap",
                    wordBreak: "break-word"
                }, children: last })] }));
}
