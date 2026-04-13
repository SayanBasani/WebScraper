import { useState } from "react";

interface itempops {
  msg: string;
  sendedBy: string;
  date: string;
  time: string;
}

export default function Chat_send({ data }: { data: itempops }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(data.msg);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch (err) {
      console.error("Copy failed", err);
    }
  };

  return (
    <>
      <div>
        <div className="justify-end flex">
          <div className="flex items-start gap-2.5">

            <div className="flex flex-col gap-1 w-full min-md:max-w-[320px] max-md:max-w-[250px] max-sm:max-w-[220px]">
              
              <div className="flex items-center space-x-2 rtl:space-x-reverse justify-end">
                <span className="text-sm font-normal">
                  {data.date} {data.time}
                </span>
                <span className="text-sm font-semibold">You</span>
              </div>

              {/* Message Bubble */}
              <div className="relative flex flex-col leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-b-xl rounded-s-xl dark:bg-gray-700">

                {/* Copy Button */}
                <button
                  onClick={handleCopy}
                  className="absolute bottom-1 right-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 text-xs"
                  title="Copy message"
                >
                  {copied ? <p className="text-xl">✓</p>: <i className="bi bi-clipboard text-xl"></i>}
                </button>

                <p className="text-sm font-normal break-words text-gray-900 dark:text-white pr-5">
                  {data.msg}
                </p>
              </div>

            </div>

            <div className="flex justify-center items-center rounded-full w-8 h-8">
              <i className="bi bi-person-circle text-2xl flex justify-center items-center"></i>
            </div>

          </div>
        </div>
      </div>
    </>
  );
}