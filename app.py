from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

TMDB_KEY = os.getenv("TMDB_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results")
def results():
    search_query = request.args.get("search_query")
    tv_show = request.args.get("tv_show") == "on"
    results = search_tmdb(search_query, tv_show)["results"]
    return render_template("results.html", results=results, tv_show=tv_show)

def search_tmdb(search_query, tv_show):
    film_search_endpoint = "https://api.themoviedb.org/3/search/movie"
    tv_search_endpont = "https://api.themoviedb.org/3/search/tv"

    headers = {"Authorization": TMDB_KEY, "accept": "application/json"}
    params = {"query": search_query}

    if not tv_show:
        response = requests.get(film_search_endpoint, headers=headers, params=params)
    else:
        response = requests.get(tv_search_endpont, headers=headers, params=params)

    return response.json()


if __name__ == "__main__":
    app.run(port=1989, debug=True)
