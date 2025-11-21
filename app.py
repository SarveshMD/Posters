from flask import Flask, render_template, url_for, request
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

TMDB_KEY = os.getenv("TMDB_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results/film")
def results_film():
    film_search_endpoint = "https://api.themoviedb.org/3/search/movie"

    headers = {"Authorization": TMDB_KEY, "accept": "application/json"}
    search_query = request.args.get("search_query")
    params = {"query": search_query}

    response = requests.get(film_search_endpoint, headers=headers, params=params)
    results = response.json()['results']
    return render_template("results_film.html", results=results)

@app.route("/results/tv")
def results_tv():
    tv_search_endpont = "https://api.themoviedb.org/3/search/tv"

    headers = {"Authorization": TMDB_KEY, "accept": "application/json"}
    search_query = request.args.get("search_query")
    params = {"query": search_query}

    response = requests.get(tv_search_endpont, headers=headers, params=params)
    results = response.json()['results']
    return render_template("results_tv.html", results=results)

if __name__ == "__main__":
    app.run(port=1989, debug=True)
