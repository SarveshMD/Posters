from extensions import db
from flask_login import UserMixin

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