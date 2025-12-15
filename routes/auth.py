from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
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

@auth_bp.route("/register", methods=["GET", "POST"])
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

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect("/")