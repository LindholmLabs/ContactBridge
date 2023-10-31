from flask import render_template
from . import web_interface

@web_interface.route('/home')
def home():
    return render_template('home.html')