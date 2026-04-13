import re
import yt_dlp

def download_youtube_video():
    try:
        url = input("Enter YouTube URL: ")

        ydl_opts = {
            'format': 'best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "Download completed successfully."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Download failed."



def download_video(url, resolution="480"):
    ydl_opts = {
        'format': f'best[height<={resolution}][ext=mp4]',
        'outtmpl': '%(title)s.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])



if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=YA0fzrnKmCs"
    # video_url = input("Enter YouTube video URL: ").strip()
    # resolution = input("Choose resolution (144 / 240 / 360 / 480 / 720): ").strip()
    resolution = "720"

    download_video(video_url, resolution)
    print(f"Download completed in {resolution}p")
