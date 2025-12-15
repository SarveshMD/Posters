from flask import Blueprint, render_template, request
from utils import tmdb_client, search_params
from flask_login import current_user
from extensions import db
from models import User, SearchLog

search_bp = Blueprint("search", __name__)

@search_bp.route("/film")
def results_film():
    film_search_endpoint = "https://api.themoviedb.org/3/search/movie"

    search_query = request.args.get("search_query")
    search_params["query"] = search_query

    response = tmdb_client.get(film_search_endpoint, params=search_params)
    results = response.json()['results']
    new_searchlog = SearchLog(logged_in=current_user.is_authenticated,
        search_query=search_query,
        film_or_tv="film",
        number_of_results=len(results),
        user=(current_user if current_user.is_authenticated else None))
    db.session.add(new_searchlog)
    db.session.commit()
    return render_template("film/results_film.html", search_query=search_query, results=results)

@search_bp.route("/tv")
def results_tv():
    tv_search_endpont = "https://api.themoviedb.org/3/search/tv"

    search_query = request.args.get("search_query")
    search_params["query"] = search_query

    response = tmdb_client.get(tv_search_endpont, params=search_params)
    results = response.json()['results']
    new_searchlog = SearchLog(logged_in=current_user.is_authenticated,
        search_query=search_query,
        film_or_tv="tv_show",
        number_of_results=len(results),
        user=(current_user if current_user.is_authenticated else None))
    db.session.add(new_searchlog)
    db.session.commit()
    return render_template("tv/results_tv.html", search_query=search_query, results=results)
