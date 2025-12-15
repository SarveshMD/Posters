from flask import Flask, render_template, url_for, request, redirect
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin
import requests
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
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
app.secret_key = os.getenv("SECRET_KEY", "fallback_key")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db_host = os.getenv("DB_HOST", "localhost")
db_pass = os.getenv("DB_PASS", "fallback_pass")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Columnn(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<'{self.id}, {self.email}, {self.password_hash}, {self.created_at}>"


class SearchLog(db.Model):
    __tablename__ = "search_logs"
    id = db.Column(db.Integer, primary_key=True)
    logged_in = db.Column(db.Boolean, nullable=False)
    search_query = db.Column(db.String(100), nullable=False)
    film_or_tv = db.Column(db.String(10), nullable=False)
    number_of_results = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    user = db.relationship("User", backref="search_logs")

    def __repr__(self):
        return f"<{self.id}, {self.logged_in}, {self.search_query}, {self.film_or_tv}, {self.number_of_results}, {self.user.email if self.user else 'Guest'}>"

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

## vvvvvvv REMOVE THESE ROUTES
@app.route("/search_history")
def search_history():
    all_logs = SearchLog.query.all()
    for log in all_logs:
        print(log)
    return redirect("/")

@app.route("/users")
def users():
    all_users = User.query.all()
    for user in all_users:
        print(user)
    return redirect("/")
## ^^^^^^ REMOVE THESE ROUTES

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return render_template("login.html", error="Incorrect email or password")

    login_user(user)
    print(user)
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

    duplicate = User.query.filter_by(email=email).first()
    if duplicate:
        return render_template("register.html", error="Email already registered")

    user = User(email=email, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    login_user(user)
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
    new_searchlog = SearchLog(logged_in=current_user.is_authenticated,
        search_query=search_query,
        film_or_tv="film",
        number_of_results=len(results),
        user=(current_user if current_user.is_authenticated else None))
    db.session.add(new_searchlog)
    db.session.commit()
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
    new_searchlog = SearchLog(logged_in=current_user.is_authenticated,
        search_query=search_query,
        film_or_tv="tv_show",
        number_of_results=len(results),
        user=(current_user if current_user.is_authenticated else None))
    db.session.add(new_searchlog)
    db.session.commit()
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

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1989, debug=True)
