import moviepy as edit
import os

def add_subtitles_to_clip(subtitles, video_name):
    os.makedirs('./output', exist_ok=True)

    baseVideo = edit.VideoFileClip('videos/' + video_name)
    
    all_clips = []
    
    for index in range(len(subtitles) - 1):
        timeCode = int(subtitles[index]['startTimeMs']) / 1000
        nextTimeCode = int(subtitles[index + 1]['startTimeMs']) / 1000
        if index >= len(subtitles) - 1:
            nextTimeCode = baseVideo.duration
        
        words = subtitles[index]['words']
        if words == '': words = '♪'
        
        txt_clip = edit.TextClip(
            text = str(words), 
            font_size = 40,
            color = 'white', 
            stroke_color = 'black', 
            stroke_width = 5,
            duration = nextTimeCode - timeCode,
        )
        
        all_clips.append(txt_clip)
    
    text_overlay = edit.concatenate_videoclips(clips = all_clips).with_start(int(subtitles[0]['startTimeMs']) / 1000).with_position(('center', 'bottom'))
    
    video = edit.CompositeVideoClip([baseVideo, text_overlay])
    video.write_videofile(
        'output/' + video_name,
        codec='libx264',
        audio_codec='aac'
    )
