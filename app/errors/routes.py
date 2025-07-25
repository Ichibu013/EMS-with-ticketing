from flask import Blueprint, render_template

from app import db

errors_bp = Blueprint('/errors', __name__, template_folder='templates')

@errors_bp.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Page Not Found'), 404

@errors_bp.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Forbidden'), 403

@errors_bp.app_errorhandler(500)
def error_500(error):
    db.session.rollback()
    return render_template('errors/500.html', title='Something Went Wrong'), 500
