interface itemProps {
  msg: string | { [key: string]: any };
  sendedBy: string;
  date: string;
  time: string;
}

export default function Chat_receive({ data }: { data: itemProps }) {
  // Safe message rendering
  const renderMessage = () => {
    if (typeof data.msg === "string") return data.msg;

    if (typeof data.msg === "object") {
      // console.log();
      if (data.msg.error) {
        return "Somthing Wrong!";
      }
      return data.msg.output;
    }

    return JSON.stringify(data.msg, null, 2);
  };

  return (
    <div>
      <div className="justify-start flex">
        <div className="flex items-start gap-2.5">
          <div className="flex justify-center items-center rounded-full w-8 h-8">
            <i className="bi bi-robot text-2xl flex justify-center items-center"></i>
          </div>
          {/* <div className="flex flex-col gap-1 w-full min-md:max-w-[320px] max-md:max-w-[250px] max-sm:max-w-[220px]"> */}
          <div className="flex flex-col gap-1 w-full max-w-[70%]">
            <div className="flex items-center space-x-2 rtl:space-x-reverse justify-start">
              <span className="text-sm font-semibold">AI</span>
              <span className="text-sm font-normal">
                {" "}
                {data.date} {data.time}{" "}
              </span>
            </div>
            <div className="flex flex-col leading-1.5 p-4 border-gray-200 bg-blue-100 rounded-b-xl rounded-e-xl dark:bg-gray-800">
              <p className="text-sm font-normal break-words text-gray-900 dark:text-white whitespace-pre-wrap">
                {renderMessage()}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
