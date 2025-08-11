import { useStorage } from "@/Storage/Storage";
import { useForm } from "react-hook-form";
import { getSummery } from "../Scraper";
import { useEffect } from "react";

export default function ChatMessagesBox() {
  const { register, handleSubmit, reset } = useForm();
  const { setchatmsg, chatmsg ,isLoading, setIsLoading} = useStorage();
  const now = new Date();

  // Format date: DD/MM/YYYY
  const date = now.toLocaleDateString("en-GB"); // '12/05/2025'

  // Format time: HH:MM AM/PM
  const time = now.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });

  const handleSendMessage = async (e: any) => {
    console.log("send messgae ------------");
    setIsLoading(true);
    const collMsg = e.collectedMessage.trim();
    if (collMsg.length == 0) return 0;
    setchatmsg((prev: any) => [
      ...prev,
      { sendedBy: "user", msg: collMsg, date, time },
    ]);
    reset();

    try {
      const summery = await getSummery(collMsg);
      setchatmsg((prev: any) => [
        ...prev,
        { sendedBy: "ai", msg: summery, date, time },
      ]);
    } catch (error) {
      console.log("Error:", error);
      setchatmsg((prev: any) => [
        ...prev,
        {
          sendedBy: "ai",
          msg: "⚠️ Failed to fetch summary. Please try again.",
          date,
          time,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // console.log(chatmsg);
  }, [chatmsg]);

  const handleKeyDown = (e: any) => {
    if (e.key == "Enter" && !e.shiftKey) {
      e.preventDefault();
      if(isLoading){return }
      handleSubmit(handleSendMessage)();
    }
  };

 return (
  <>
    <div className={`w-full px-2 pb-1 h-full ${isLoading ? "" : ""}`}>
      <form
        onSubmit={handleSubmit(handleSendMessage)}
        className={`${
          isLoading ? "bg-gray-500" : ""
        } h-full w-full pl-3 pr-1 py-1 rounded-3xl border border-gray-200 items-center gap-2 inline-flex justify-between`}>
        
        {/* Input Area */}
        <div className="flex items-center gap-2 w-full justify-center px-3">
          <textarea
            {...register("collectedMessage", { maxLength: 1000 })}
            onKeyDown={handleKeyDown}
            className={`msgTextArea h-[25px] text-x custom-textarea grow shrink basis-0 text-white leading-4 focus:outline-none`}
            placeholder="Type here..."
          ></textarea>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2">
          <i className="bi bi-paperclip text-xl rotate-45"></i>

          {isLoading ? (
            // Loader when isLoading is true
            <div className="w-6 h-6 border-2 border-white border-t-indigo-500 animate-spin rounded-full"></div>
          ) : (
            // Send button when not loading
            <button
              type="submit"
              title="send button"
              className="cursor-pointer items-center flex px-3 py-2 bg-indigo-600 rounded-full shadow ">
              <i className="bi bi-send text-sm"></i>
            </button>
          )}
        </div>
      </form>
    </div>
  </>
);

}
