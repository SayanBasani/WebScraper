# from google_crc32c import exc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time , os ,re, shutil
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def retrieve_page(url,path = 'retriev_pages/index.html'):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome( service=Service(ChromeDriverManager().install()), options=options )
        driver.get(url)
        print("\n" + driver.title + "\n")
        html = driver.page_source
        
        with open(path, 'w', encoding='utf-8') as file:  
            file.write(driver.page_source)
        
        driver.quit()
        print("Page retrieved and saved successfully.")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return html
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# from bs4 import BeautifulSoup
def clear_code(path_of_code='retriev_pages/index.html',path = 'retriev_pages/index.txt'):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path_of_code, 'r', encoding='utf-8', errors='replace') as file:
            page_code = file.read()
        
        soup = BeautifulSoup(page_code, "html.parser")
        all_text = soup.get_text(separator="")
        clear_text = ' '.join(all_text.split())
        with open(path,'w',encoding='utf-8') as file:
            file.write(clear_text)
        print("Code cleared and saved successfully.")
        return clear_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# marge the retrival and the cleaning functions
def get_page_txt(url, html_path='retriev_pages/index.html', txt_path='retriev_pages/index.txt'):
    try:
        file_name = 'retriev_pages/'+re.sub(r'[<>:/\\;"\'{}[\]|?*]', "_", url)
        retrieve_page(url, path=file_name+'.html')
        clened_txt = clear_code(file_name+'.html', file_name+'.txt')
        # shutil.rmtree('retriev_pages', ignore_errors=True) # clean up the retriev_pages folder after use
        return clened_txt
    except Exception as e:
        print(f"An error occurred in get_page_txt: {e}")
        return {"error": str(e)}


import yt_dlp

def download_video(url, resolution="480", output_path="downloads"):
    try:
        
        os.makedirs(output_path, exist_ok=True)

        ydl_opts = {
            'format': f'best[height<={resolution}][ext=mp4]/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True,
            'cookiefile': 'cookies.txt', 
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            # Video title (name)
            title = info.get("title")

            # Actual downloaded filename
            file_path = ydl.prepare_filename(info)
            file_name = os.path.basename(file_path)

        return {
            "message": f"Download completed in {resolution}p",
            "video_title": title,
            "file_name": file_name,
            "full_path": os.path.abspath(file_path)
        }

    except Exception as e:
        return {"error": str(e)}

from django.http import JsonResponse
from django.http import FileResponse, Http404
from django.conf import settings

def download_video_info_(request):
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

def download_video_info(url,resolution="480",output_path="downloads"):
    # url = request.data.get("url")
    # print(request)
    # url = request.data.get("q", "").strip()
    # quality = request.data.get("quality", "360") | request.data.get("resolution","360")
    print(f"Downloading video from URL: {url} with resolution: {resolution}p")
    if not url:
        return JsonResponse({"error": "URL is required"}, status=400)
    download_video_resp = download_video(url, resolution, output_path)
    
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


if __name__ == "__main__":
    result = download_video(
        "https://youtu.be/vdtTEdj4cQ8",
        resolution="1080"
    )
    print(result)
