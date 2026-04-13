import { useStorage } from "@/Storage/Storage";
import { useForm } from "react-hook-form";
import { useState } from "react";
import { getSummery } from "@/Storage/BackendRequests";

export default function ChatMessagesBox() {
  const [isSending, setIsSending] = useState(false);
  const { register, handleSubmit, reset } = useForm();
  const { setchatmsg } = useStorage();

  // 🕒 Generate fresh time per message
  const getTimeData = () => {
    const now = new Date();

    return {
      date: now.toLocaleDateString("en-GB"),
      time: now.toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
        hour12: true,
      }),
    };
  };

  const handleSendMessage = async (e: any) => {
    if (isSending) return;

    const collMsg = e.collectedMessage?.trim();
    if (!collMsg) return;

    setIsSending(true);

    const { date, time } = getTimeData();

    // 👤 User message
    setchatmsg((prev: any) => [
      ...prev,
      {
        sendedBy: "user",
        msg: collMsg,
        date,
        time,
        return_type: "user Message",
      },
    ]);

    reset();

    try {
      const summery = await getSummery(collMsg);

      // 🎬 Video response
      if (summery?.return_type?.toLowerCase() === "video") {
        const videoUrl =
          "http://127.0.0.1:8000" +
          summery.download_url +
          "?file=" +
          encodeURIComponent(summery.file_name);

        setchatmsg((prev: any) => [
          ...prev,
          {
            sendedBy: "ai",
            msg: {
              message: collMsg,
              response: {
                type: "video",
                content: videoUrl,
              },
            },
            ...getTimeData(),
          },
        ]);
      } else {
        // 💬 Normal response
        setchatmsg((prev: any) => [
          ...prev,
          {
            sendedBy: "ai",
            msg: summery,
            ...getTimeData(),
          },
        ]);
      }
    } catch (error) {
      console.error("Error:", error);

      setchatmsg((prev: any) => [
        ...prev,
        {
          sendedBy: "ai",
          msg: "⚠️ Failed to fetch summary. Please try again.",
          ...getTimeData(),
        },
      ]);
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyDown = (e: any) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!isSending) {
        e.currentTarget.form?.requestSubmit();
      }
    }
  };

  return (
    <div className="w-full px-2 pb-1 h-full">
      <form
        onSubmit={handleSubmit(handleSendMessage)}
        className={`${
          isSending ? "bg-gray-500" : ""
        } h-full w-full pl-3 pr-1 py-1 rounded-3xl border border-gray-200 items-center gap-2 inline-flex justify-between`}
      >
        {/* Input */}
        <div className="flex items-center gap-2 w-full justify-center px-3">
          <textarea
            {...register("collectedMessage", { maxLength: 1000 })}
            onKeyDown={handleKeyDown}
            className="msgTextArea h-[25px] text-x custom-textarea grow shrink basis-0 text-white leading-4 focus:outline-none"
            placeholder="Type here..."
          />
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <i className="bi bi-paperclip text-xl rotate-45"></i>

          {isSending ? (
            <div className="w-6 h-6 border-2 border-white border-t-indigo-500 animate-spin rounded-full"></div>
          ) : (
            <button
              type="submit"
              title="send button"
              className="cursor-pointer items-center flex px-3 py-2 bg-indigo-600 rounded-full shadow"
            >
              <i className="bi bi-send text-sm"></i>
            </button>
          )}
        </div>
      </form>
    </div>
  );
}