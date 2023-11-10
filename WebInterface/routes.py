import json
from pathlib import Path
from flask import request, redirect, url_for, render_template, session
from . import web_interface


@web_interface.route('/')
@web_interface.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('web_interface.login'))

    messages_context = {
        "api_endpoint": "messages",
        "id_prefix": "message-",
        "headers": [("ID", "10%"), ("Relevance", "20%"), ("Name", "30%"), ("Content", "40%")]
    }

    spam_context = {
        "api_endpoint": "messages",
        "id_prefix": "spam-",
        "headers": [("ID", "10%"), ("Relevance", "10%"), ("Name", "30%"), ("Content", "50%")]
    }

    return render_template('/page/home.html', page_title='Messages', messages_context=messages_context, spam_context=spam_context)


@web_interface.route('/integrations')
def integrations():
    return render_template('/page/integrations.html', page_title="Integrations")


@web_interface.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        current_dir = Path(__file__).parent
        settings_path = current_dir / '..' / 'settings.json'
        with open(settings_path, 'r') as f:
            settings = json.load(f)

        if username == settings['username'] and password == settings['password']:
            session['logged_in'] = True
            return redirect(url_for('web_interface.home'))
        else:
            return "Invalid credentials", 401

    return render_template('login.html')


@web_interface.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('web_interface.login'))
