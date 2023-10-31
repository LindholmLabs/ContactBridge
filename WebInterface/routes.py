from flask import render_template

from  dbrepository import DatabaseRepository
from . import web_interface

db = DatabaseRepository()

@web_interface.route('/home')
def home():
    messages = db.fetch_messages()

    formatted_messages = [
        {
            "id": message[0],
            "name": message[1],
            "email": message[2],
            "subject": message[3],
            "message_content": message[4],
            "timestamp": message[5]
        }
        for message in messages
    ]

    return render_template('home.html', messages=formatted_messages)