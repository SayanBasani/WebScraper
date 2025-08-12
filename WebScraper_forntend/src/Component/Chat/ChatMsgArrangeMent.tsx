import Chat_send from "./Chat_send";
import Chat_recive from "./Chat_recive";
import { useStorage } from "@/Storage/Storage";

export default function ChatMsgArrangeMent() {
  const { chatmsg } = useStorage();
  // console.log(chatmsg);
  return (
    <>
      <div className="grid gap-2">
        {chatmsg.map((item: any, index: number) => {
          if (item.sendedBy == "user") {
            return (
              <>
                <Chat_send data={item} key={item.id || index} />
              </>
            );
          }
          if (item.sendedBy == "ai") {
            return (
              <>
                <Chat_recive data={item} key={item.id || index} />
              </>
            );
          }
        })}
      </div>
    </>
  );
}
