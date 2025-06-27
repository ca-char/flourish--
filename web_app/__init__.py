from flask import Flask
from config import Config
from web_app.extensions import db, login_manager, csrf
from web_app.models import User
from web_app.routes import views, auth
from web_app.db_management import create_db, insert_sample_data

def create_app(config_overrides=None, test_config=None):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    if config_overrides:
        app.config.update(config_overrides)

    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        create_db(reset=True)

        if app.config.get("LOAD_SAMPLE_DATA"):
            if User.query.count() == 0:
                insert_sample_data()
                
        if not test_config:
            if User.query.count() == 0:
                insert_sample_data()

    return app
