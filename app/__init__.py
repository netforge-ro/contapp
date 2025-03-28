from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        from app.routes import facturi, furnizori, stocuri, clienti, rapoarte, dashboard
        
        app.register_blueprint(facturi.bp)
        app.register_blueprint(furnizori.bp)
        app.register_blueprint(stocuri.bp)
        app.register_blueprint(clienti.bp)
        app.register_blueprint(rapoarte.bp)
        app.register_blueprint(dashboard.bp)
        
        db.create_all()
        
    return app
