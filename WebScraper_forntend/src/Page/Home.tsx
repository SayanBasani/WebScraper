// app/home/page.tsx (for Next.js 13+ App Router)
// or use as a component in any React project

import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();
  const navi_chat = ()=>{navigate("/chat");}
  return (
    <div className="w-full min-h-screen flex items-center justify-center p-4 text-white">
      <div className="w-full max-w-xl border border-gray-200 rounded-xl shadow-md p-6 text-center space-y-4">
        <h2 className="font-bold text-3xl">
          Smart AI Summarizer & Chat Assistant
        </h2>
        <p className="text-gray-700">
          Paste a website link or ask a question.
        </p>
        <p className="text-gray-600">
          Get smart summaries or instant answers from AI.
        </p>
        <input
          type="text"
          placeholder="Paste link or type your question..."
          className="w-full mt-4 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button type="button" onClick={navi_chat} className="mt-3 w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg">
          Analyze
        </button>
      </div>
    </div>
  );
}
