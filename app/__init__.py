from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from app.config import Config

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Cho phép mọi domain truy cập (Bỏ qua lỗi CORS)
    CORS(app)
    
    mongo.init_app(app)
    
    with app.app_context():
        from app.controllers.scenario_controller import scenario_bp
        app.register_blueprint(scenario_bp)
        
    return app
