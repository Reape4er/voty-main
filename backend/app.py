from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from models import *

from routes.auth import auth_bp
from routes.events import events_bp
from routes.nominations import nominations_bp
from routes.protocol import protocol_bp
from routes.scores import scores_bp
from routes.users import users_bp
from routes.applications import applications_bp
from routes.criteria import criteria_bp
from routes.result import result_bp

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your-secret-key"

jwt = JWTManager(app)

db.init_app(app)
with app.app_context():
    db.create_all()

# Регистрация Blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(events_bp)  # url_prefix='/events' использвоать потом
app.register_blueprint(nominations_bp) 
app.register_blueprint(protocol_bp)
app.register_blueprint(scores_bp)
app.register_blueprint(users_bp)
app.register_blueprint(applications_bp)
app.register_blueprint(criteria_bp)
app.register_blueprint(result_bp) 
