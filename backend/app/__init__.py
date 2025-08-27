from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app) 

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app) 

    with app.app_context():
        from . import models   
        db.create_all()

    from .routes import main
    app.register_blueprint(main)

    return app