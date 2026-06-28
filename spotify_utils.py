import requests

def get_song_details(track_name, artist_name):
    try:
        query  = f"{track_name} {artist_name}"
        url    = "https://itunes.apple.com/search"
        params = {"term": query, "media": "music", "limit": 1, "entity": "song"}
        res    = requests.get(url, params=params, timeout=5).json()

        if res["resultCount"] > 0:
            item    = res["results"][0]
            img_url = item.get("artworkUrl100", "").replace("100x100", "300x300")
            preview = item.get("previewUrl", None)
            return img_url, preview

    except Exception:
        pass

    return None, None