from MessageTagging.spam_detector import SpamDetector
from . import api
from flask_restx import Resource, fields

from dbrepository import DatabaseRepository
from .mailer import Mailer

mailer = Mailer()
db_repo = DatabaseRepository()
spam_detection = SpamDetector()

contact_fields = api.model('Contact', {
    'email': fields.String(required=True),
    'name': fields.String(required=True),
    'message_content': fields.String(required=True)
})

@api.route('/contact')
class contact(Resource):
    @api.expect(contact_fields)
    def post(self):
        data = api.payload
        email = data['email']
        name = data['name']
        message_content = data['message_content']

        formatted_subject = mailer.format_subject(email)
        formatted_message = mailer.format_message(name, email, message_content)

        prediction = spam_detection.detect_spam(message_content)
        rounded_prediction = float(f'{prediction:.2f}')

        if prediction < .05:
            try:
                mailer.send_notification(formatted_subject, formatted_message)
            except Exception as e:
                return {"message": f"An unknown error occurred: {str(e)}"}, 500

        db_repo.save_message(name, email, formatted_subject, message_content, rounded_prediction)

        return {"message": "Message sent and saved successfully"}, 200


@api.route('/messages')
class Messages(Resource):
    def get(self):
        messages = db_repo.fetch_messages()
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
        return formatted_messages, 200