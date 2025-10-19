import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Initialize Spotify client with client credentials (no user login needed)
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_track(query):
    results = sp.search(q=query, type='track', limit=3)
    for idx, track in enumerate(results['tracks']['items']):
        print(f"{idx + 1}. {track['name']} by {track['artists'][0]['name']}")
        print(f"   Album: {track['album']['name']}")
        print(f"   Preview URL: {track['preview_url']}")
        print()

if __name__ == '__main__':
    search_term = input("Enter song or artist name to search: ")
    search_track(search_term)
