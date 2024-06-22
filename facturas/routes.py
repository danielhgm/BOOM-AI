from flask import Blueprint, render_template, request
from app.models import User  # Si estás utilizando modelos
main_bp = Blueprint('main', __name__)
@main_bp.route('/')
def index():
    return render_template('index.html')
    
@main_bp.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)