from flask import Flask, render_template, url_for, request
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

TMDB_KEY = os.getenv("TMDB_API_KEY")

film_endpoint = "https://api.themoviedb.org/3/movie"
headers = {"Authorization": TMDB_KEY, "accept": "application/json"}
search_params = {"query": None}
img_params = {"include_image_language": "en-US"}

def fetch_film(id):
    response = requests.get(f"{film_endpoint}/{id}", headers=headers, timeout=10)
    return response.json()

def fetch_images(id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{id}/images", headers=headers, params=img_params, timeout=10)
    return response.json()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results/film")
def results_film():
    film_search_endpoint = "https://api.themoviedb.org/3/search/movie"

    search_query = request.args.get("search_query")
    search_params["query"] = search_query

    response = requests.get(film_search_endpoint, headers=headers, params=search_params)
    results = response.json()['results']
    return render_template("results_film.html", search_query=search_query, results=results)

@app.route("/results/tv")
def results_tv():
    tv_search_endpont = "https://api.themoviedb.org/3/search/tv"

    search_query = request.args.get("search_query")
    search_params["query"] = search_query

    response = requests.get(tv_search_endpont, headers=headers, params=search_params)
    results = response.json()['results']
    return render_template("results_tv.html", search_query=search_query, results=results)

@app.route("/film/<id>")
def film_page(id):
    data = fetch_film(id)
    images = fetch_images(id)
    return render_template("film_page.html", data=data, posters=images['posters'])


@app.route("/film/<id>/posters")
def film_posters(id):
    data = fetch_film(id)
    images = fetch_images(id)

    return render_template("film_posters.html", data=data, posters=images['posters'])
# → full_posters.html

@app.route("/film/<id>/backdrops")
def film_backdrops(id):
    data = fetch_film(id)
    images = fetch_images(id)

    return render_template("film_backdrops.html", data=data, backdrops=images['backdrops'])
# → full_backdrops.html


@app.route("/film/<id>/logos")
def film_logos(id):
    data = fetch_film(id)
    images = fetch_images(id)

    return render_template("film_logos.html", data=data, logos=images['logos'])
# → full_logos.html

if __name__ == "__main__":
    app.run(port=1989, debug=True)
