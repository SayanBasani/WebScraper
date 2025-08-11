import Chat_send from "./Chat_send";
import Chat_recive from "./Chat_recive";
import { useStorage } from "@/Storage/Storage";

export default function ChatMsgArrangeMent() {
  const { chatmsg } = useStorage();
  // console.log(chatmsg);
  return (
    <>
      <div className="grid gap-2">
        {chatmsg.map((item: any) => {
          if (item.sendedBy == "user") {
            return (
              <>
                <Chat_send data={item} />
              </>
            );
          }
          if (item.sendedBy == "ai") {
            return (
              <>
                <Chat_recive data={item} />
              </>
            );
          }
        })}
      </div>
    </>
  );
}
