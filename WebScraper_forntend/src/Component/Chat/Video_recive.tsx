// https://chatgpt.com/c/69536a55-e69c-8322-a1c1-bc473c8050db work with this chat gpt chat
interface AIResponse {
  type: "text" | "video";
  content: string; // text OR video URL
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

export default function Video_receive({ data }: { data: itemProps }) {
  // console.log(data);
  const renderContent = () => {
    // Plain string (fallback)
    if (typeof data.msg === "string") {
      return (
        <p className="text-sm text-gray-900 whitespace-pre-wrap">{data.msg}</p>
      );
    }

    // Error
    if (data.msg.error) {
      return <p className="text-sm text-red-500">Something went wrong ❌</p>;
    }

    const response = data.msg.response;

    // TEXT RESPONSE
    if (response?.type === "text") {
      return (
        <p className="text-sm text-gray-900 whitespace-pre-wrap">
          {response.content}
        </p>
      );
    }

    // VIDEO RESPONSE
    if (response?.type === "video") {
      return (
        <div className="flex flex-col gap-2">
          <video
            src={response.content}
            controls
            className="w-full max-w-md rounded-lg bg-black"
            preload="metadata"
          />

          <a
            href={response.content}
            download
            className="self-start text-sm text-blue-600 hover:underline">
            Download video
          </a>
        </div>
      );
    }

    // Fallback
    return (
      <pre className="text-xs text-gray-700">
        {JSON.stringify(data.msg, null, 2)}
      </pre>
    );
  };

  return (
    <div className="flex justify-start">
      <div className="flex items-start gap-2.5 max-w-[70%]">
        <div className="flex justify-center items-center rounded-full w-8 h-8">
          <i className="bi bi-robot text-2xl" />
        </div>

        <div className="flex flex-col gap-1 w-full">
          <div className="flex items-center gap-2">
            <span className="text-sm font-semibold">AI</span>
            <span className="text-sm text-gray-500">
              {data.date} {data.time}
            </span>
          </div>

          <div className="p-4 bg-blue-100 rounded-b-xl rounded-e-xl">
            {renderContent()}
          </div>
        </div>
      </div>
    </div>
  );
}
