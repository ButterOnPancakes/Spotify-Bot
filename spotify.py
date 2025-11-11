import base64
import requests
import json
import os

from os.path import join, dirname
from dotenv import load_dotenv

from syrics.api import Spotify


def get_token():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')

    if not client_id or not client_secret:
        raise Exception("CLIENT_ID or CLIENT_SECRET not found in environment variables")

    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    
    try:
        result = requests.post(url, headers=headers, data=data, timeout=10)
        result.raise_for_status()  # Raises HTTPError for bad responses
        json_results = result.json()
        token = json_results['access_token']
        return token
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to get Spotify token: {e}")

def get_auth_headers(token):
    return {'Authorization': 'Bearer ' + token}

def search_artist(token, artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_headers(token)
    query = f'?q={artist_name}&type=artist&limit=1'
    
    query_url = url + query
    
    try:
        result = requests.get(query_url, headers=headers, timeout=10)
        result.raise_for_status()
        json_results = result.json()
        artists = json_results['artists']['items']
        
        if len(artists) == 0:
            raise Exception(f'No artists called "{artist_name}" has been found in the spotify api.')
        
        return artists[0]
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to search artist: {e}")

def get_songs_by_artist(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US'
    headers = get_auth_headers(token)
    
    try:
        result = requests.get(url, headers=headers, timeout=10)
        result.raise_for_status()
        json_results = result.json()
        tracks = json_results['tracks']
        
        return tracks
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to get artist tracks: {e}")

def get_song_by_name(token, song_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_headers(token)
    query = f'?q={song_name}&type=track&limit=1'
    
    query_url = url + query
    
    try:
        result = requests.get(query_url, headers=headers, timeout=10)
        result.raise_for_status()
        json_results = result.json()
        tracks = json_results['tracks']['items']
        
        if not tracks:
            raise Exception(f"No tracks found for '{song_name}'")
            
        return tracks
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to search song: {e}")

def get_songs_subtitles(song_id):
    dotenv_path = join(dirname(__file__), '.env')  # Changed from '.variables' to '.env'
    load_dotenv(dotenv_path)

    spdc = os.environ.get('SP_DC')
 
    sp = Spotify(spdc)

    lyrics_data = sp.get_lyrics(song_id)

    if lyrics_data:
        print("Lyrics successfully downloaded")
        return lyrics_data
    else:
        raise Exception("No lyrics found for this track.")



