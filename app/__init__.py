from flask import Flask
from config import Config
import os


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(os.path.join(
        os.getcwd(), app.config['UPLOAD_FOLDER']), exist_ok=True)

    from app.routes import main
    app.register_blueprint(main)

    return app
