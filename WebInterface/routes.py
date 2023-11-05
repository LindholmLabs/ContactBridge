import json
from pathlib import Path

from flask import Flask, request, redirect, url_for, render_template, session
from dbrepository import DatabaseRepository
from . import web_interface
from .tableBuilder import TableBuilder

db = DatabaseRepository()


@web_interface.route('/')
@web_interface.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('web_interface.login'))

    messages = db.fetch_messages()

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
    # Define headers and rows for the messages table
    headers = ["ID", "Message", "Date", "Delete"]
    rows = [
        [1, "Hello World!", "2023-11-01"],
        [2, "Another Message", "2023-11-02"],
    ]

    def delete_link(row_data):
        # Assuming row_data is a dictionary that contains an 'id' key
        id = row_data[0]
        # Return a string of HTML. The 'material-icons' class is used for Material Icons
        return f'<a href="/message/delete/{id}" class="delete-icon"><i class="material-icons">delete</i></a>'

    # Initialize TableBuilder and configure the table
    table_builder = TableBuilder()
    table_builder.set_headers(headers)
    table_builder.add_rows(rows)
    table_builder.set_pagination(enabled=True, page_size=5)
    table_builder.set_sortable(["ID", "Date"])
    table_builder.add_callback_column(delete_link)
    table_builder.set_on_click("/message/{0}")

    # Build the TableInstance
    table_instance = table_builder.build()
    return render_template('integrations.html', page_title="Integrations", table=table_instance)

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
