import spotify
import downloadYT
import editing
import os

def karaoke_with_clip(token, song_name):
    print('Getting lyrics from the Spotify API...')
    song = spotify.get_song_by_name(token, song_name)[0]
    print(f"Found song: {song['name']} by {song['artists'][0]['name']}")
    
    subtitles = spotify.get_songs_subtitles(song['id'])['lyrics']['lines']
    print(f"Retrieved {len(subtitles)} subtitle lines")
    print('---------------------------------------\n')
    
    print('Searching for video on YouTube...')
    videoID = downloadYT.searchVideo(f"{song['name']} {song['artists'][0]['name']}")
    print(f"Found video ID: {videoID}")
    
    print('Downloading video...')
    downloadYT.downloadVideo("https://www.youtube.com/watch?v=" + videoID)
    print('Download completed')
    print('---------------------------------------\n')
    
    print('Adding subtitles to video...')
    output_file = editing.add_subtitles_to_clip(subtitles, videoID + '.mp4')
    print(f'Done! Check the file: {output_file}')

    # Clean up - only remove if file exists and processing was successful
    try:
        video_path = './videos/' + videoID + '.mp4'
        if os.path.exists(video_path):
            os.remove(video_path)
            print("Temporary video file cleaned up")
    except Exception as e:
        print(f"Warning: Could not clean up temporary file: {e}")

if __name__ == '__main__':
    try:
        token = spotify.get_token()
        print("Successfully authenticated with Spotify")
        
        song_name = input('What song? : ').strip()
        if not song_name:
            print("Please enter a valid song name")
        else:
            karaoke_with_clip(token, song_name)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Fatal error: {e}")
