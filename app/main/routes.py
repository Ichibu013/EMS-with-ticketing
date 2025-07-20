from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__, template_folder = 'templates')

@main_bp.route('/')
@main_bp.route('/home')
def home():
    # PlaceHolder for events
    return render_template('main/home.html',title='Home')

@main_bp.route('/dashboard')
def dashboard():
    # User-specific dashboard
    return render_template('main/dashboard.html',title='Dashboard')