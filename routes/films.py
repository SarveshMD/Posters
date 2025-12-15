from flask import Blueprint, render_template, request
from utils import tmdb_client, fetch_tmdb, film_endpoint, img_params
from flask_login import current_user
from extensions import db
from models import User, SearchLog

films_bp = Blueprint('films', __name__)

@films_bp.route("/<id>")
def film_page(id):
    data = fetch_tmdb(f"{film_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/movie/{id}/images", params=img_params)
    return render_template("film/film_page.html", data=data, posters=images['posters'])

@films_bp.route("/<id>/posters")
def film_posters(id):
    data = fetch_tmdb(f"{film_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/movie/{id}/images", params=img_params)

    return render_template("film/film_posters.html", data=data, posters=images['posters'])

@films_bp.route("/<id>/backdrops")
def film_backdrops(id):
    data = fetch_tmdb(f"{film_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/movie/{id}/images", params=img_params)

    return render_template("film/film_backdrops.html", data=data, backdrops=images['backdrops'])

@films_bp.route("/<id>/logos")
def film_logos(id):
    data = fetch_tmdb(f"{film_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/movie/{id}/images", params=img_params)

    return render_template("film/film_logos.html", data=data, logos=images['logos'])
