# Importing the necessary libraries
from requests import post
from PIL import Image
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import base64


# Spotify API
scope = "user-read-currently-playing,user-modify-playback-state"
client_id = "Replace ME"
client_secret = "Replace ME"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost"))

# First variables for the job function 
# Get current playing track
track = sp.current_user_playing_track()
if track == None:
    track = '{"error": "No song playing"}'
else:
    # Get album art url
    album_art_url = track['item']['album']['images'][0]['url']
    # Get song name
    song_name = track['item']['name']
    # Get artist name
    artist_name = track['item']['artists'][0]['name']
    # Get album name
    album_name = track['item']['album']['name']
    # Get song duration
    song_duration = track['item']['duration_ms']
    # Get song progress
    song_progress = track['progress_ms']
    # Get song progress percentage
    song_progress_percentage = (song_progress / song_duration) * 100
    # Get song progress in seconds
    song_progress_seconds = song_progress / 1000
    # Get song duration in seconds
    song_duration_seconds = song_duration / 1000
    # Get song progress in minutes
    song_progress_minutes = song_progress_seconds / 60
    # Get song duration in minutes
    song_duration_minutes = song_duration_seconds / 60

# Flask Setup
from flask import Flask
app = Flask(__name__)



# Spotify Now Playing API
@app.route('/spotify/nowplaying')
def spotify_nowplaying():
    return str(track)

# Spotify Album Art API
@app.route('/spotify/albumart')
def spotify_albumart():
    return str(album_art_url)

# Spotify Song Name API
@app.route('/spotify/songname')
def spotify_songname():
    return str(song_name)

# Spotify Artist Name API
@app.route('/spotify/artistname')
def spotify_artistname():
    return str(artist_name)

# Spotify Album Name API
@app.route('/spotify/albumname')
def spotify_albumname():
    return str(album_name)

# Spotify Song Duration API
@app.route('/spotify/songduration')
def spotify_songduration():
    return str(song_duration)

# Spotify Song Progress API
@app.route('/spotify/songprogress')
def spotify_songprogress():
    return str(song_progress)

# Spotify Song Progress Percentage API
@app.route('/spotify/songprogress/percentage')
def spotify_songprogresspercentage():
    return str(song_progress_percentage)

# Spotify Song Progress Seconds API
@app.route('/spotify/songprogress/seconds')
def spotify_songprogressseconds():
    return str(song_progress_seconds)

# Spotify Song Duration Seconds API
@app.route('/spotify/songduration/seconds')
def spotify_songdurationseconds():
    return str(song_duration_seconds)

# Spotify Song Progress Minutes API
@app.route('/spotify/songprogress/minutes')
def spotify_songprogressminutes():
    return str(song_progress_minutes)

# Spotify Song Duration Minutes API
@app.route('/spotify/songduration/minutes')
def spotify_songdurationminutes():
    return str(song_duration_minutes)

# Spotify Play/Pause API
@app.route('/spotify/playpause')
def spotify_playpause():
    sp.pause_playback()
    return "{\"status\": \"success\"}"

# Spotify Next Song API
@app.route('/spotify/next')
def spotify_next():
    sp.next_track()
    return "{\"status\": \"success\"}"

# Spotify Previous Song API
@app.route('/spotify/previous')
def spotify_previous():
    sp.previous_track()
    return "{\"status\": \"success\"}"

# Spotify Shuffle API
@app.route('/spotify/shuffle')
def spotify_shuffle():
    sp.shuffle(True)
    return "{\"status\": \"success\"}"

# Get Colours Of Album Art
@app.route('/spotify/albumart/colours')
def spotify_albumart_colours():
    # Get album art
    response = requests.get(album_art_url)
    # Save album art to bytes
    img = Image.open(BytesIO(response.content))
    # Resize album art to 30x30 pixels
    img = img.resize((30, 30))
    # Get colours of album art
    colours = img.getcolors(900)
    # Return colours
    return str(colours)

# Serve Album Art 30x30
@app.route('/spotify/albumart/30x30.png')
def spotify_albumart_3x3():
    # Get album art
    response = requests.get(album_art_url)
    # Save album art to bytes
    img = Image.open(BytesIO(response.content))
    # Resize album art to 3x3 pixels
    img = img.resize((30, 30))
    # Save album art to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    # Return album art as html image
    return "<img src=\"data:image/png;base64," + str(img_str)[2:-1] + "\"/>"    


# Human Readble Song Info
@app.route('/spotify')
def spotify():
    return str("Song: " + song_name + "\nArtist: " + artist_name + "\nAlbum: " + album_name)





# Background Scheduler 
def job():
    ## Bakcground Scheduler to run every 5 seconds
    # Set all variables to global
    global track
    global album_art_url
    global song_name
    global artist_name
    global album_name
    global song_duration
    global song_progress
    global song_progress_percentage
    global song_progress_seconds
    global song_duration_seconds
    global song_progress_minutes
    global song_duration_minutes
    # Get current playing track
    track = sp.current_user_playing_track()
    if track == None:
        track = '{"error": "No song playing"}'
    # Get album art url
    album_art_url = track['item']['album']['images'][0]['url']
    # Get song name
    song_name = track['item']['name']
    # Get artist name
    artist_name = track['item']['artists'][0]['name']
    # Get album name
    album_name = track['item']['album']['name']
    # Get song duration
    song_duration = track['item']['duration_ms']
    # Get song progress
    song_progress = track['progress_ms']
    # Get song progress percentage
    song_progress_percentage = (song_progress / song_duration) * 100
    # Get song progress in seconds
    song_progress_seconds = song_progress / 1000
    # Get song duration in seconds
    song_duration_seconds = song_duration / 1000
    # Get song progress in minutes
    song_progress_minutes = song_progress_seconds / 60
    # Get song duration in minutes
    song_duration_minutes = song_duration_seconds / 60



# Background Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(job, 'interval', seconds=10)
scheduler.start()
