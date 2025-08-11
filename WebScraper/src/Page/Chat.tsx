import ChatMessagesBox from "@/Component/Chat/ChatMessagesBox";
import ChatMsgArrangeMent from "@/Component/Chat/ChatMsgArrangeMent";

export default function Chat() {
  return (
    // <div className="flex flex-col w-full h-full">
    <div className="grid grid-rows-[1fr_50px] h-full w-full">
      <div className="flex flex-col-reverse py-4 overflow-y-auto">
        <ChatMsgArrangeMent />
      </div>
      <div className="">
        <ChatMessagesBox />
      </div>
    </div>
  );
}
