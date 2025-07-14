from flask import Blueprint

from .auth_routes import auth_bp
from .usr_routes import usr_bp
from .cziber_routes import cziber_bp
from .empresa_routes import empresa_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(usr_bp, url_prefix="/user")
    app.register_blueprint(cziber_bp, url_prefix="/cziber")
    app.register_blueprint(empresa_bp, url_prefix="/company")