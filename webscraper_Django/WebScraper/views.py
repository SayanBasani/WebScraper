from calendar import c
import re
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
# from sympy import im, per
# from torch import ge
from .Ext_Fnx import manage_conversation, function_map, ai_usage_manager
import json


@api_view(['GET'])
@permission_classes([AllowAny])
def hello():
    return Response({"msg":"Hello"})
ai_model = 'chatgpt'  # 'chatgpt' or 'gemini'
conversation=[]
@api_view(['POST'])
@permission_classes([AllowAny])
def aiRequest(request):
    try:
        print(request.data)
        user_message = request.data.get("q", "").strip()
        if not user_message:
            return Response({ "message": "AI Request Failed", "response": { "type": "error", "content": "Empty message received." } }, status=400)
        manage_conversation(role="user", message=user_message, conversation=conversation, ai=ai_model)
        # resp = geminiGOOGLE(conversation, client, tools=gemini_tools)
        resp = ai_usage_manager(conversation, ai_model)
        print("AI Response:", resp)
        
        if resp["return_type"] == "function":
            # respMsg = "Function call requested: " + ", ".join(resp["tools"])
            tool_calls = resp.get("tools", [])
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
                    manage_conversation(role="assistant", message=json.dumps(result_json), conversation=conversation, ai=ai_model)
                    print(result_json)
                    # it is for the video download function which returns a file path, we need to convert it to a download url
                    if fn_name == "download_video_info":
                        return result
            manage_conversation(role="user", message="Function(s) executed successfully and the responces are provided by the assistent", conversation=conversation, ai=ai_model)
            # resp = geminiGOOGLE(conversation, client, tools=gemini_tools)
            resp = ai_usage_manager(conversation, ai_model)
            print("AI Response after function execution:", resp)
            respMsg = resp.get("content", "")
            # respMsg = resp["content"]
            resp_msg_str = respMsg if isinstance(respMsg, str) else str(respMsg)
            # return Response({ "message": "AI Request Received!", "response": { "type": resp["return_type"], "content": resp_msg_str } }, status=200)
            return Response({ "message": "AI Request Received!", "response": { "type": "text", "content": resp_msg_str } }, status=200)
        elif resp["return_type"] == "error":
            respMsg = "Error: " + resp["content"]
        else:
            respMsg = resp["content"]
    
        resp_msg_str = respMsg if isinstance(respMsg, str) else str(respMsg)
        # conversation.append({"role":"assistant", "content":resp_msg_str} ) 
        if resp_msg_str.strip() != "":
            manage_conversation(role="assistant", message=resp_msg_str, conversation=conversation, ai=ai_model)
        # return Response({ "message": "AI Request Received!", "response": { "type": resp["return_type"], "content": resp_msg_str } }, status=200)
        return Response({ "message": "AI Request Received!", "response": { "type": "text", "content": resp_msg_str } }, status=200)
    except Exception as e:
        print("Error in aiRequest:", str(e))
        return Response({ "message": "Error processing AI request.", "error": str(e) }, status=500) 

import os
from django.http import FileResponse, JsonResponse
from django.conf import settings


from .functions import download_video
@api_view(['POST'])
@permission_classes([AllowAny])
def download_video_info(request):
    # url = request.data.get("url")
    print(request.data)
    url = request.data.get("q", "").strip()
    quality = request.data.get("quality", "360")
    if not url:
        return JsonResponse({"error": "URL is required"}, status=400)
    download_video_resp = download_video(url, quality, "downloads")
    
     # ✅ HANDLE ERROR FIRST
    if "error" in download_video_resp:
        return JsonResponse({
            "error": download_video_resp["error"]
        }, status=500)
    file_name = download_video_resp["file_name"]
    video_path = settings.BASE_DIR /"downloads" /file_name
    if not video_path.exists():
        return JsonResponse({"error": "File not found"}, status=404)
    file_size = os.path.getsize(video_path)
    
    if not video_path.exists():
        return JsonResponse({"error": "File not found"}, status=404)
    resp = {
        "file_name": download_video_resp["file_name"],
        "file_size": file_size,
        "file_path": str(video_path),
        "download_url":"/ai/download/",
        "return_type":"video",
    }
    print("Download Video Info Response:", resp)
    return JsonResponse(resp)

# views.py
from django.http import FileResponse, Http404
from django.conf import settings

def download_video_file(request):
    file_name = request.GET.get("file")

    if not file_name:
        raise Http404("File name required")

    video_path = settings.BASE_DIR / "downloads" / file_name

    if not video_path.exists():
        raise Http404("File not found")

    response = FileResponse(
        open(video_path, "rb"),
        content_type="video/mp4"
    )
    response["Content-Length"] = video_path.stat().st_size
    response["Content-Disposition"] = f'attachment; filename="{file_name}"'
    print("Video file download response prepared successfully")
    print(response)
    return response


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def download_video_info1(request):
    # url = request.data.get("url")
    print(request.data)
    url = request.data.get("q", "").strip()
    quality = request.data.get("quality", "360")
    if not url:
        return JsonResponse({"error": "URL is required"}, status=400)
    download_video_resp = download_video(url, quality, "downloads")
    
     # ✅ HANDLE ERROR FIRST
    if "error" in download_video_resp:
        return JsonResponse({
            "error": download_video_resp["error"]
        }, status=500)
    file_name = download_video_resp["file_name"]
    video_path = settings.BASE_DIR /"downloads" /file_name
    if not video_path.exists():
        return JsonResponse({"error": "File not found"}, status=404)
    file_size = os.path.getsize(video_path)
    
    if not video_path.exists():
        return JsonResponse({"error": "File not found"}, status=404)
    resp = {
        "file_name": download_video_resp["file_name"],
        "file_size": file_size,
        "file_path": str(video_path),
        "download_url":"/ai/download/",
        "return_type":"video",
    }
    print("Download Video Info Response:", resp)
    return JsonResponse(resp)
