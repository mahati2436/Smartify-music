from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# Load .env variables
load_dotenv()

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Updated Track model
class Track(BaseModel):
    name: str
    artist: str
    album: str
    preview_url: str | None
    image_url: str | None  # New field for album cover

# Spotify client setup
client_credentials_manager = SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# ✅ Updated search route
@app.get("/search", response_model=list[Track])
async def search_tracks(query: str = Query(..., min_length=1)):
    results = sp.search(q=query, type="track", limit=5)
    tracks = []
    for item in results["tracks"]["items"]:
        image_url = item["album"]["images"][0]["url"] if item["album"]["images"] else None
        tracks.append(Track(
            name=item["name"],
            artist=item["artists"][0]["name"],
            album=item["album"]["name"],
            preview_url=item["preview_url"],
            image_url=image_url
        ))
    return tracks

# Serve frontend static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")
