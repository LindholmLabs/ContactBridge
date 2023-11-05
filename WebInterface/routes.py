import json
from pathlib import Path

from flask import Flask, request, redirect, url_for, render_template, session
from dbrepository import DatabaseRepository
from . import web_interface
from .tableBuilder import TableBuilder
from .tableFactory import TableFactory

db = DatabaseRepository()


@web_interface.route('/')
@web_interface.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('web_interface.login'))

    messages = db.get_all_messages()

    formatted_messages = [
        {
            "id": message[0],
            "name": message[1],
            "email": message[2],
            "subject": message[3],
            "message_content": message[4],
            "timestamp": message[5],
            "relevance": message[6]
        }
        for message in messages
    ]

    return render_template('home.html', messages=formatted_messages, page_title="Messages")


@web_interface.route('/integrations')
def integrations():
    page_number = request.args.get('page', 1, type=int)

    tables = TableFactory()
    message_table = tables.get_message_table(page_number)

    return render_template('integrations.html', page_title="Integrations", table=message_table)

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
