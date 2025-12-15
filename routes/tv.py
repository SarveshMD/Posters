from flask import Blueprint, render_template, request
from utils import tmdb_client, fetch_tmdb, tv_endpoint, img_params
from flask_login import current_user
from extensions import db
from models import User, SearchLog

tv_bp = Blueprint('tv', __name__)

@tv_bp.route("/<id>")
def tv_page(id):
    data = fetch_tmdb(f"{tv_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/tv/{id}/images", params=img_params)
    return render_template("tv/tv_page.html", data=data, posters=images['posters'])

@tv_bp.route("/<id>/posters")
def tv_posters(id):
    data = fetch_tmdb(f"{tv_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/tv/{id}/images", params=img_params)

    return render_template("tv/tv_posters.html", data=data, posters=images['posters'])

@tv_bp.route("/<id>/backdrops")
def tv_backdrops(id):
    data = fetch_tmdb(f"{tv_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/tv/{id}/images", params=img_params)

    return render_template("tv/tv_backdrops.html", data=data, backdrops=images['backdrops'])

@tv_bp.route("/<id>/logos")
def tv_logos(id):
    data = fetch_tmdb(f"{tv_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/tv/{id}/images", params=img_params)

    return render_template("tv/tv_logos.html", data=data, logos=images['logos'])
