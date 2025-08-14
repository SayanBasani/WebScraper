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
        document.addEventListener("selectionchange", () => {
            const selection = window.getSelection();
            const selectedText = selection ? selection.toString() : "";
            console.log("Selected text:", selectedText);
        });
    }, []);
    return (_jsxs("div", { style: { padding: 12, width: 280, fontFamily: "system-ui, sans-serif" }, children: [_jsx("h2", { style: { margin: "0 0 8px" }, children: "Web Scraper" }), _jsx("p", { style: { margin: "0 0 8px" }, children: "Toolbar popup is working \uD83C\uDF89" }), _jsxs("p", { style: { margin: "0 0 6px", fontSize: 12, opacity: 0.8 }, children: ["Uptime: ", time, "s"] }), _jsx("div", { style: {
                    padding: "8px 10px",
                    background: "#f5f5f7",
                    borderRadius: 8,
                    minHeight: 50,
                    whiteSpace: "pre-wrap",
                    wordBreak: "break-word",
                }, children: last })] }));
}
