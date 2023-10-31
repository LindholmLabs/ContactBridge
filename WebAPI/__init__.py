from flask import Flask
from flask_restx import Resource, Api, fields

from WebAPI.mailer import *

app = Flask(__name__)
api = Api(app)

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

        formatted_subject = format_subject(email)
        formatted_message = format_message(name, email, message_content)

        send_email(formatted_subject, formatted_message)

if __name__ == '__main__':
    app.run(debug=True)