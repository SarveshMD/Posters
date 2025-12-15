import requests
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

load_dotenv()

film_endpoint = "https://api.themoviedb.org/3/movie"
tv_endpoint = "https://api.themoviedb.org/3/tv"
search_params = {"query": None}
img_params = {"include_image_language": "en-US"}

def create_robust_session():
    session = requests.Session()

    retry = Retry(
        total=3,
        read=3,
        connect=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504]
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
        "Authorization": os.getenv("TMDB_API_KEY")
    })

    return session

tmdb_client = create_robust_session()

def fetch_tmdb(endpoint, params=None):
    response = tmdb_client.get(endpoint, params=params)
    return response.json()
