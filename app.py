from flask import Flask, render_template, url_for, request, redirect
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin
import requests
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

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

app = Flask(__name__)
app.secret_key = "COFFEE_PLUS_COCOA"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, email, password_hash):
        self.id = id
        self.email = email
        self.password_hash = password_hash

    def __str__(self):
        return f"('{self.id}, {self.email}, {self.password_hash})"

temp_users = {}
test_user = User(id=1, email="johndoe@example.com", password_hash=generate_password_hash("pass"))
temp_users[test_user.email] = test_user

film_endpoint = "https://api.themoviedb.org/3/movie"
tv_endpoint = "https://api.themoviedb.org/3/tv"
search_params = {"query": None}
img_params = {"include_image_language": "en-US"}

def fetch_tmdb(endpoint, params=None):
    response = tmdb_client.get(endpoint, params=params)
    return response.json()

@app.route("/")
def index():
    return render_template("index.html")

@login_manager.user_loader
def load_user(user_id):
    for u in temp_users.values():
        if str(u.id) == str(user_id):
            return u
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")
    user = temp_users.get(email)

    if not user or not check_password_hash(user.password_hash, password):
        return render_template("login.html", error="Incorrect email or password")

    login_user(user)
    print((email, password))
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    email = request.form.get("email")
    password = request.form.get("password")
    confirm = request.form.get("confirm_password")

    if password != confirm:
        return render_template("register.html", error="Passwords do not match")

    user = User(len(temp_users) + 1, email, generate_password_hash(password))
    temp_users[user.email] = user
    login_user(user)
    print((email, password))
    for user in temp_users:
        print(temp_users[user])
    return redirect("/")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/results/film")
def results_film():
    film_search_endpoint = "https://api.themoviedb.org/3/search/movie"

    search_query = request.args.get("search_query")
    search_params["query"] = search_query

    response = tmdb_client.get(film_search_endpoint, params=search_params)
    results = response.json()['results']
    return render_template("film/results_film.html", search_query=search_query, results=results)

@app.route("/film/<id>")
def film_page(id):
    data = fetch_tmdb(f"{film_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/movie/{id}/images", params=img_params)
    return render_template("film/film_page.html", data=data, posters=images['posters'])


@app.route("/film/<id>/posters")
def film_posters(id):
    data = fetch_tmdb(f"{film_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/movie/{id}/images", params=img_params)

    return render_template("film/film_posters.html", data=data, posters=images['posters'])

@app.route("/film/<id>/backdrops")
def film_backdrops(id):
    data = fetch_tmdb(f"{film_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/movie/{id}/images", params=img_params)

    return render_template("film/film_backdrops.html", data=data, backdrops=images['backdrops'])


@app.route("/film/<id>/logos")
def film_logos(id):
    data = fetch_tmdb(f"{film_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/movie/{id}/images", params=img_params)

    return render_template("film/film_logos.html", data=data, logos=images['logos'])

@app.route("/results/tv")
def results_tv():
    tv_search_endpont = "https://api.themoviedb.org/3/search/tv"

    search_query = request.args.get("search_query")
    search_params["query"] = search_query

    response = tmdb_client.get(tv_search_endpont, params=search_params)
    results = response.json()['results']
    return render_template("tv/results_tv.html", search_query=search_query, results=results)

@app.route("/tv/<id>")
def tv_page(id):
    data = fetch_tmdb(f"{tv_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/tv/{id}/images", params=img_params)
    return render_template("tv/tv_page.html", data=data, posters=images['posters'])


@app.route("/tv/<id>/posters")
def tv_posters(id):
    data = fetch_tmdb(f"{tv_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/tv/{id}/images", params=img_params)

    return render_template("tv/tv_posters.html", data=data, posters=images['posters'])

@app.route("/tv/<id>/backdrops")
def tv_backdrops(id):
    data = fetch_tmdb(f"{tv_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/tv/{id}/images", params=img_params)

    return render_template("tv/tv_backdrops.html", data=data, backdrops=images['backdrops'])


@app.route("/tv/<id>/logos")
def tv_logos(id):
    data = fetch_tmdb(f"{tv_endpoint}/{id}")
    images = fetch_tmdb(f"https://api.themoviedb.org/3/tv/{id}/images", params=img_params)

    return render_template("tv/tv_logos.html", data=data, logos=images['logos'])


if __name__ == "__main__":
    app.run(port=1989, debug=True)
