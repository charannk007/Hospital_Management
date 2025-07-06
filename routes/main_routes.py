from flask import Blueprint, render_template
from config.settings import get_hospital_name
from datetime import datetime

main = Blueprint('main', __name__)

# This runs before rendering any template and adds variables globally
@main.context_processor
def inject_hospital_info():
    return {
        'hospital_name': get_hospital_name(),
        'year': datetime.now().year
    }

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/privacy')
def privacy():
    return render_template('privacy.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/careers')
def careers():
    return render_template('coming_soon.html', hospital_name=get_hospital_name(), year=datetime.now().year)

@main.route('/networks')
def networks():
    return render_template('coming_soon.html', hospital_name=get_hospital_name(), year=datetime.now().year)

@main.route('/blog')
def blog():
    return render_template('coming_soon.html', hospital_name=get_hospital_name(), year=datetime.now().year)

@main.route('/events')
def events():
    return render_template('coming_soon.html', hospital_name=get_hospital_name(), year=datetime.now().year)
