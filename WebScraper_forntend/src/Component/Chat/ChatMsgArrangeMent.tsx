import Chat_send from "./Chat_send";
import Chat_recive from "./Chat_recive";
import { useStorage } from "@/Storage/Storage";
import Video_receive from "./Video_recive";

export default function ChatMsgArrangeMent() {
  const { chatmsg } = useStorage();
  // console.log(chatmsg);
  return (
    <>
      <div className="grid gap-2">
        {chatmsg.map((item: any, index: number) => {
          // console.log(chatmsg)
          console.log(item)
          // console.log(`${item.return_type}---${item.msg?.response?.type}`)
          if (item.sendedBy == "user") {
            return (
              <>
                <Chat_send data={item} key={item.id || index} />
              </>
            );
          }
          else if(item.sendedBy === "ai" && item.msg?.response?.type === "video"){
            return (
              <>
                <Video_receive data={item} key={item.id || index} />
              </>
            );
          }
          else if (item.sendedBy == "ai") {
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
