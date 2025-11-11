from __future__ import unicode_literals
import re
from yt_dlp import YoutubeDL

VIDEO_SAVE_DIRECTORY = "videos"
AUDIO_SAVE_DIRECTORY = "audios"

def searchVideo(video_name):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{video_name}", download=False)
            if info and 'entries' in info and len(info['entries']) > 0:
                return info['entries'][0]['id']
            else:
                raise Exception("No video found for the search query")
    except Exception as e:
        print(f"Error searching for video: {e}")
        return old_search(video_name)

def old_search(video_name):
    import urllib.request
    search = '+'.join(video_name.lower().split())
    
    html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={search}")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    
    if not video_ids:
        raise Exception("No video IDs found in search results")
    
    return video_ids[0]

def downloadAudio(url):
    audio_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{AUDIO_SAVE_DIRECTORY}/%(id)s.%(ext)s',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(audio_opts) as ydl:
        ydl.download([url])

def downloadVideo(url):
    video_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': f'{VIDEO_SAVE_DIRECTORY}/%(id)s.%(ext)s',
        'noplaylist': True,
    }
    with YoutubeDL(video_opts) as ydl:
        ydl.download([url])
