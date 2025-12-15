from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # we pass in 'app' here?
login_manager = LoginManager()
