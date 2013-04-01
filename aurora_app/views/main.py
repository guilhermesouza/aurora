from flask import Blueprint, render_template

mod = Blueprint('main', __name__)


@mod.route('/')
def index():
    return render_template('main/login.html')


@mod.route('/login')
def login():
    return render_template('main/login.html')
