from flask import Blueprint, redirect
from models import User, SearchLog

debug_bp = Blueprint('debug', __name__)

## vvvvvvv REMOVE THESE ROUTES
@debug_bp.route("/search_history")
def search_history():
    all_logs = SearchLog.query.all()
    for log in all_logs:
        print(log)
    return redirect("/")

@debug_bp.route("/users")
def users():
    all_users = User.query.all()
    for user in all_users:
        print(user)
    return redirect("/")
## ^^^^^^ REMOVE THESE ROUTES