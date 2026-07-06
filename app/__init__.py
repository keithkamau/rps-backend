from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .config import Config

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    socketio.init_app(app, message_queue=None)
    migrate.init_app(app, db)
    limiter.init_app(app)
    CORS(app, origins=[app.config['FRONTEND_URL']])
    
    from .routes.auth import auth_bp
    from .routes.game import game_bp
    from .routes.tournament import tournament_bp
    from .routes.admin import admin_bp
    from .routes.spectator import spectator_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(game_bp, url_prefix='/api/game')
    app.register_blueprint(tournament_bp, url_prefix='/api/tournament')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(spectator_bp, url_prefix='/api/spectator')
    
    return app
