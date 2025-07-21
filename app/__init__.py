from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' #specify using route
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register Blueprint(Controller)
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Main blueprint
    from app.main.routes import main_bp
    app.register_blueprint(main_bp)

    # Event blueprint
    from app.event.routes import event_bp
    app.register_blueprint(event_bp)

    # Ticket blueprint
    from app.ticket.routes import ticket_bp
    app.register_blueprint(ticket_bp)

    # Admin blueprint
    from app.admin.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app