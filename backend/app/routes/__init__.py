from flask import Blueprint

from .auth_routes import auth_bp
from .admin_routes import admin_bp
from .employee_routes import employee_bp
from .query_routes import query_bp
from .empresa_routes import empresa_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(employee_bp, url_prefix="/employee")
    app.register_blueprint(query_bp, url_prefix="/query")
    app.register_blueprint(empresa_bp, url_prefix="/empresa")