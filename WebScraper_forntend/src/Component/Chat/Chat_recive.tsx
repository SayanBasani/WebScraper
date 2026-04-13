import { useState } from "react";

interface AIResponse {
  type: string;
  content: string;
}

interface MessageObject {
  message: string;
  response: AIResponse;
  error?: string;
}

interface itemProps {
  msg: MessageObject | string;
  sendedBy: string;
  date: string;
  time: string;
}

export default function Chat_receive({ data }: { data: itemProps }) {
  const [copied, setCopied] = useState(false);

  // Safe message rendering
  const renderMessage = () => {
    if (typeof data.msg === "string") return data.msg;
    if (data.msg.response?.content) return data.msg.response.content;
    if (data.msg?.error) return "Something went wrong!";
    return JSON.stringify(data.msg, null, 2);
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(renderMessage());
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch (err) {
      console.error("Copy failed", err);
    }
  };

  return (
    <div>
      <div className="justify-start flex">
        <div className="flex items-start gap-2.5">
          
          <div className="flex justify-center items-center rounded-full w-8 h-8">
            <i className="bi bi-robot text-2xl flex justify-center items-center"></i>
          </div>

          <div className="flex flex-col gap-1 w-full max-w-[70%]">
            
            <div className="flex items-center space-x-2 rtl:space-x-reverse justify-start">
              <span className="text-sm font-semibold">AI</span>
              <span className="text-sm font-normal">
                {data.date} {data.time}
              </span>
            </div>

            {/* Message Bubble */}
            <div className="relative flex flex-col leading-1.5 p-4 border-gray-200 bg-blue-100 rounded-b-xl rounded-e-xl dark:bg-gray-800">

              {/* Copy Button */}
              <button
                onClick={handleCopy}
                className="absolute bottom-1 right-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 text-xs"
                title="Copy message"
              >
                {copied ? (
                  <span className="text-green-500 text-xl">✓</span>
                ) : (
                  <i className="text-xl bi bi-clipboard"></i>
                )}
              </button>

              <p className="text-sm font-normal break-words text-gray-900 dark:text-white whitespace-pre-wrap pr-5">
                {renderMessage()}
              </p>

            </div>

          </div>
        </div>
      </div>
    </div>
  );
}