from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ask import Ask
import os

parent_dir = os.path.dirname(os.path.abspath(__file__))
templates_folder = os.path.join(parent_dir, "templates")
sql_db = SQLAlchemy()
ask = Ask(route="/alexa_app")


def create_app(config_file):
    app = Flask(__name__, template_folder=templates_folder)
    app.config.from_pyfile(config_file)
    ask.init_app(app)
    sql_db.init_app(app)
    from project.app.skills.movie_skills import views
    from project.app.skills.computer_skills import views
    return app



