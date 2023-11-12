from datetime import datetime

from flask import request
from flask_restx import Namespace, Resource, fields

from MessageTagging.spam_detector import SpamDetector
from WebAPI.utils.mailer import Mailer
from database.models.messages import MessageModel
from database.models.spam import SpamModel
from database.repository import DbRepository

contact_ns = Namespace('contact', description='Contact namespace, used for integration with external sites.')

db_repository = DbRepository()
message_model = MessageModel()
spam_model = SpamModel()
mailer = Mailer()
sd = SpamDetector()

message_create_model = contact_ns.model('Contact', {
    'name': fields.String(required=True, description='The senders name'),
    'email': fields.String(required=True, description='The email address of the sender'),
    'content': fields.String(required=True, description='The content of the message'),
})


@contact_ns.route('/')
class ContactResource(Resource):

    @contact_ns.expect(message_create_model)
    def post(self):
        """Contact form endpoint"""
        try:
            data, subject, content = prepare_data()
            inverted_relevance = calculate_relevance(data['content'])
        except Exception as e:
            return {'message': 'Invalid data'}, 400

        try:
            parameters = (
                data['name'],
                data['email'],
                data.get('subject', 'No subject'),
                data['content'],
                inverted_relevance
            )

            if inverted_relevance > 0.5:
                message_model.create(parameters)
                mailer.send_notification(subject, content)
            else:
                spam_model.create(parameters)

            return {'message': 'Message saved successfully'}, 201
        except Exception as e:
            print(f"An error occurred: {e}")
            return {'message': 'An error occurred while processing your request'}, 500


def calculate_relevance(content):
    try:
        relevance = float(sd.detect_spam(content))
        return round(1 - relevance, 2)
    except Exception as e:
        print(f"An error occurred in relevance calculation: {e}")
        return 1


def prepare_data():
    if request.json:
        form_data = request.json
    else:
        form_data = request.form

    name = form_data['name']
    email = form_data['email']
    content = form_data['content']

    subject = f"{name} Has contacted you from {email} at {datetime.now().time()}"
    return form_data, subject, content