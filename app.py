from flask import Flask, render_template, url_for, request, redirect
import os
from models import User
from extensions import db, login_manager

from routes.main import main_bp
from routes.auth import auth_bp
from routes.debug import debug_bp
from routes.search import search_bp
from routes.films import films_bp
from routes.tv import tv_bp

def create_app():
    app = Flask(__name__)

    app.secret_key = os.getenv("SECRET_KEY", "fallback_key")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.session.get(int(user_id))

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(debug_bp)
    app.register_blueprint(search_bp, url_prefix="/results")
    app.register_blueprint(films_bp, url_prefix="/film")
    app.register_blueprint(tv_bp, url_prefix="/tv")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=1989, debug=True)
