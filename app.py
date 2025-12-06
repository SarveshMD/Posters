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
    return render_template("results_film.html", search_query=search_query, results=results)

@app.route("/results/tv")
def results_tv():
    tv_search_endpont = "https://api.themoviedb.org/3/search/tv"

    headers = {"Authorization": TMDB_KEY, "accept": "application/json"}
    search_query = request.args.get("search_query")
    params = {"query": search_query}

    response = requests.get(tv_search_endpont, headers=headers, params=params)
    results = response.json()['results']
    return render_template("results_tv.html", search_query=search_query, results=results)

@app.route("/film/<id>")
def film_page(id):
    film_endpoint = "https://api.themoviedb.org/3/movie/"

    headers = {"Authorization": TMDB_KEY, "accept": "application/json"}

    response = requests.get(f"{film_endpoint}/{id}", headers=headers, timeout=5)
    data = response.json()
    params = {'include_image_language': 'en-US'}
    images = requests.get(f"https://api.themoviedb.org/3/movie/{id}/images", headers=headers, params=params, timeout=5).json()

    print(images['posters'])
    return render_template("film_page.html", data=data, posters=images['posters'])


@app.route("/film/<id>/posters")
def film_posters(id):
    pass
# → full_posters.html

@app.route("/film/<id>/backdrops")
def film_backdrops(id):
    pass
# → full_backdrops.html

@app.route("/film/<id>/logos")
def film_logos(id):
    pass
# → full_logos.html

if __name__ == "__main__":
    app.run(port=1989, debug=True)
