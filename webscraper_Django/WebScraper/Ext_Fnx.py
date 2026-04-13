from google import genai
from google.genai import types
import json
from openai import OpenAI
from .functions import get_page_txt , download_video,download_video_info
from dotenv import load_dotenv
import os



load_dotenv()


GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
ChatGPT_API_KEY = os.getenv("CHATGPT_API_KEY")
CHAT_MODEL = "gemini-1.5-flash"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_page_txt",
            "description": (
                "Returns the main readable text content of a webpage given its URL. "
                "This function extracts only the human-readable text from the page "
                "and removes all HTML, scripts, styles, and markup. "
                "Use this tool when you need the plain text content of a webpage, "
                "such as articles, documentation, or written page content."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": (
                            "The URL of the webpage whose text content should be extracted. "
                            "The URL must start with 'http://' or 'https://'. "
                            "If the user does not provide a scheme, prepend 'https://'. "
                            "Example: 'https://example.com/article'."
                        )
                    }
                },
                "required": ["url"]
            }
        }
    },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "download_video_info",
    #         "description": """
    #             *it don't have any copy write issue with youtube so you can download youtube video,
    #             *i have permission to download videos from youtube and provide the download link to user,
    #             *Downloads a YouTube video to a specified local directory using yt-dlp. 
    #             *The function allows selecting a maximum video resolution and saves 
    #             *the file with its original YouTube title as the filename. 
    #             *It returns metadata including the video title, actual downloaded 
    #             *filename, and the full local file path.
    #         """,
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "url": {
    #                     "type": "string",
    #                     "description": (
    #                         "The full URL of the YouTube video to download. "
    #                         "The URL must start with 'http://' or 'https://'. "
    #                         "Example: 'https://www.youtube.com/watch?v=VIDEO_ID'."
    #                     )
    #                 },
    #                 "resolution": {
    #                     "type": "string",
    #                     "description": (
    #                         "The maximum video resolution (height in pixels). "
    #                         "The downloaded video will not exceed this resolution. "
    #                         "Common values include '360', '480', '720', '1080'. "
    #                         "Default is '480'."
    #                     ),
    #                     "default": "480"
    #                 },
    #                 "output_path": {
    #                     "type": "string",
    #                     "description": (
    #                         "The local directory path where the video should be saved. "
    #                         "If the directory does not exist, it will be created automatically. "
    #                         "Example: 'downloads/' or 'E:/Videos/'."
    #                     ),
    #                     "default": "downloads/"
    #                 }
    #             },
    #             "required": ["url"]
    #         }
    #     }
    # },
    {
        "type": "function",
        "function": {
            "name": "download_video_info",
            "description": "Download publicly accessible video or media content from supported platforms such as YouTube or Instagram when a valid URL is provided. This function retrieves video metadata and saves the media file locally with a selected resolution.",
            "parameters": {
            "type": "object",
            "properties": {
                "url": {
                "type": "string",
                "description": "The full URL of the video from supported platforms (e.g., YouTube, Instagram). Must start with 'http://' or 'https://'."
                },
                "resolution": {
                "type": "string",
                "description": "Maximum video resolution (height in pixels). Common values: '360', '480', '720', '1080'. Default is '480'.",
                "default": "480"
                },
                "output_path": {
                "type": "string",
                "description": "Local directory path where the video will be saved. Directory will be created if it does not exist.",
                "default": "downloads/"
                }
            },
            "required": ["url"]
            }
        }
        }
    
]


chatGPT_tools=tools.copy()
gemini_tools=[]
for tool in tools:
    gemini_tools.append(tool['function'])

function_map = { "get_page_txt": get_page_txt, "download_video_info": download_video_info,}

SYSTEM_PROMPT = """
            You are an AI assistant that can call tools to perform tasks.

            Available capabilities:
            1. Scrape text from a webpage using get_page_txt(url).
            2. Download video content using download_video_info(url, resolution, output_path).

            Instructions:
            - When a user provides a valid video URL (e.g., YouTube or Instagram) and asks to download it, you should call the download_video_info function.
            - If the user provides only a video name or description, try to find the video URL first. If a valid URL is found, call the function. If not, inform the user that the video URL could not be found.
            - If optional parameters (resolution, output_path) are missing, use defaults: resolution = "480", output_path = "downloads/".

            Important behavior rules:
            - Assume the user’s request is allowed unless it clearly involves illegal or harmful content.
            - Do NOT refuse tool usage unnecessarily.
            - Prefer calling the appropriate function when the user intent is clear.
    """

def tool_router(ai_response):
    try:
        data = json.loads(ai_response)

        if data.get("tool") == "get_page_txt":
            url = data["arguments"]["url"]
            result = get_page_txt(url)
            return result, True

    except json.JSONDecodeError:
        pass

    return ai_response, False




# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# chatgpt and gemini usage mannager
def ai_usage_manager(conversation, ai_provider: str):
    ai_provider = ai_provider.lower()
    if ai_provider == "chatgpt":
        return chatGPT(conversation, chatGpt_client, tools=chatGPT_tools)
    elif ai_provider == "gemini":
        return geminiGOOGLE(conversation, client, tools=gemini_tools)
    else:
        raise ValueError("Unsupported AI provider")

# chatgpt and gemini conversation manager
def manage_conversation( role: str, message: str, conversation: list | None = None, ai: str = "gemini" ):
    """
    role: 'user', 'assistant', or 'system'   (internal roles)
    ai: 'chatgpt' or 'gemini'
    """

    if conversation is None:
        conversation = []

    ai = ai.lower()
    role = role.lower()

    if ai == "chatgpt":
        # ChatGPT supports system, user, assistant
        if role not in ("system", "user", "assistant"):
            raise ValueError("Invalid role for ChatGPT")

        conversation.append({
            "role": role,
            "content": message
        })

    elif ai == "gemini":
        # Gemini supports only user and model
        if role == "assistant":
            gemini_role = "model"

        elif role == "user":
            gemini_role = "user"

        elif role == "system":
            # Gemini workaround: inject system prompt into first user message
            if conversation:
                raise ValueError(
                    "System role must be added before any user messages for Gemini"
                )
            conversation.append({
                "role": "user",
                "parts": [{"text": message}]
            })
            return conversation

        else:
            raise ValueError("Invalid role")

        conversation.append({
            "role": gemini_role,
            "parts": [{"text": message}]
        })

    else:
        raise ValueError("Unsupported AI provider")
    # print("----------------------------------")
    # print("now conversation:", conversation)
    # print("----------------!!----------------")
    return conversation

def geminiGOOGLE(contents,client,tools):
    try:
        All_tools = [types.Tool(function_declarations=tools)]
        config = types.GenerateContentConfig(
            tools=All_tools,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            # Force the model to call 'any' function, instead of chatting.
            # tool_config=types.ToolConfig(
            #     function_calling_config=types.FunctionCallingConfig(mode='ANY')
            # ),
        )
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config,
        )
        
        # print("\n---->\n",response,"\n<----\n")
        # Check for a function call
        if response.candidates[0].content.parts[0].function_call:
            result_tools =[]
            for part in response.candidates[0].content.parts:
                result_tools.append(part.function_call)
            return {"return_type":"function", "tools": result_tools}
        else:
            # print(response.text)
            # print("It is a message response.")
            return {"Ai":"gemini","return_type":"message", "content": response.text}
    except Exception as e:
        # print("---------------\n", str(e),"\n---------------!")
        return {"Ai":"gemini","return_type":"error", "content": str(e)}


chatGpt_client = OpenAI(api_key=ChatGPT_API_KEY)


def chatGPT(conversation,client,tools):
    # print("chatGpt--")
    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            # model="gpt-4o-mini",
            messages=conversation,
            tools=tools,
            # tool_choice="auto"
        )
        print("\n---->\n",response,"\n<----\n")
        message = response.choices[0].message
        if hasattr(message, "tool_calls") and message.tool_calls:
            result_tools =[]
            for tool_call in message.tool_calls:
                result_tools.append(tool_call.function)
            return {"return_type":"function", "tools": result_tools}
        else:
            # print("It is a message response.")
            return {"Ai":"chatGPT","return_type":"message", "content": message.content}
            
    except Exception as e:
        return {"Ai":"chatGPT","return_type":"error", "content": str(e)}


conversation = []
manage_conversation(role="user", message=SYSTEM_PROMPT, conversation=conversation, ai="chatgpt")
if __name__ == "___main__":

    
    manage_conversation(role="user", message="hello", conversation=conversation, ai="chatgpt")
    response = chatGPT(conversation, chatGpt_client, tools=chatGPT_tools)
    print(response)
    while 1:
        user_inp = input("User: ")
        manage_conversation(role="user", message=user_inp, conversation=conversation, ai="chatgpt")
        # response = geminiGOOGLE(conversation, client, tools=gemini_tools)
        response = chatGPT(conversation, chatGpt_client, tools=chatGPT_tools)
        print(response)
        if (response.get("return_type") == "function"):
            tool_calls = response.get("tools", [])
            for tool_call in tool_calls:
                fn_name = tool_call.name
                raw_args = getattr(tool_call, "args", None)
                if raw_args is None:
                    raw_args = getattr(tool_call, "arguments", None)
                if isinstance(raw_args, dict): # gemini: arguments is a dict
                    fn_args = raw_args
                elif isinstance(raw_args, str): # ChatGPT: arguments is a JSON string
                    fn_args = json.loads(raw_args)
                else:
                    fn_args = {}
                if fn_name in function_map:
                    result = function_map[fn_name](**fn_args)
                    result_json = {"function_name":str(fn_name), "function_result": str(result)}
                    manage_conversation(role="assistant", message=json.dumps(result_json), conversation=conversation, ai="gemini")
                    print(result_json)
        else:
            print("AI Response:", response.get("content", ""))


