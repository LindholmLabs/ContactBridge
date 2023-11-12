from flask import request, render_template, make_response, jsonify
from flask_restx import Namespace, Resource, fields

from MessageTagging.spam_detector import SpamDetector
from WebAPI.utils.mailer import Mailer
from database.models.messages import MessageModel
from database.models.spam import SpamModel
from database.repository import DbRepository

spam_ns = Namespace('spam', description='Spam operations')

db_repository = DbRepository()
spam_model = SpamModel()
message_model = MessageModel()
mailer = Mailer()
sd = SpamDetector()

spam_read_model = spam_ns.model('Spam', {
    'id': fields.Integer(readOnly=True, description='The message unique identifier'),
    'name': fields.String(required=True, description='The senders name'),
    'email': fields.String(required=True, description='The email address of the sender'),
    'subject': fields.String(required=False, description='The subject of the message'),
    'content': fields.String(required=True, description='The content of the message'),
    'timestamp': fields.String(required=True, description='The time at which the message was sent'),
    'relevance': fields.Float(readOnly=True, description='relevance, tries to set to low values for spam')
})

@spam_ns.route('/')
class MessageList(Resource):

    @spam_ns.doc('get_messages')
    @spam_ns.response(400, "sort_order must be either 'ASC' or 'DESC'")
    @spam_ns.response(400, "Invalid sort_by field. Must be one of {sort fields}")
    @spam_ns.response(406, "Invalid accept header. Must be one of {valid_accept_headers}, received: {accept_header}")
    @spam_ns.param('query', 'search query')
    @spam_ns.param('sort_by', 'Field to sort the messages by')
    @spam_ns.param('sort_order', 'Order to sort the messages (ASC or DESC)')
    @spam_ns.param('page', 'The page to retrieve')
    @spam_ns.param('page_size', 'The number of messages to retrieve per page')
    @spam_ns.produces(['application/json', 'text/html'])
    def get(self):
        """Get (paginated) messages (HTML or JSON)"""
        args = request.args
        query = args.get('query', '', type=str)
        page = args.get('page', 1, type=int)
        page_size = args.get('page_size', 10, type=int)
        sort_by = args.get('sort_by', 'id')  # Default sort by 'id'
        sort_order = args.get('sort_order', 'ASC').upper()  # Default sort order 'ASC'

        messages, total_pages = spam_model.get_page(page, page_size, sort=sort_by, sort_order=sort_order,
                                                       search=query)
        accept_header = request.headers.get('Accept', '')

        if sort_order not in ['ASC', 'DESC']:
            spam_ns.abort(400, "sort_order must be either 'ASC' or 'DESC'")

        valid_sort_fields = ['id', 'name', 'email', 'subject', 'timestamp', 'relevance', 'content']
        if sort_by not in valid_sort_fields:
            spam_ns.abort(400, f"Invalid sort_by field. Must be one of {valid_sort_fields}")

        valid_accept_headers = ['', 'text/html', 'application/json']
        if accept_header not in valid_accept_headers:
            spam_ns.abort(406,
                              f"Invalid accept header. Must be one of {valid_accept_headers}, received: {accept_header}")

        if 'text/html' in accept_header:
            response = make_response(render_template('component/messages_template.html', messages=messages))
            response.headers['X-Total-Pages'] = total_pages
            response.headers['X-Current-Page'] = page
            return response
        else:
            response = make_response(jsonify(messages))
            response.headers['X-Total-Pages'] = total_pages
            response.headers['X-Current-Page'] = page
            return response


@spam_ns.route('/<int:id>')
@spam_ns.response(404, 'Message not found')
class Message(Resource):
    @spam_ns.marshal_with(spam_read_model)
    def get(self, id):
        """Get a message"""
        message = spam_model.get(id)
        if message:
            return message, 200
        else:
            spam_ns.abort(404, "Message not found")

    @spam_ns.response(204, 'Message deleted')
    @spam_ns.response(404, 'Message not found')
    def delete(self, id):
        """Delete a message"""
        message = spam_model.get(id)
        if not message:
            spam_ns.abort(404, "Message not found")

        try:
            spam_model.delete(id)
            return make_response('', 204)
        except Exception as e:
            spam_ns.abort(500, "An internal error occurred")
        """Delete a message by id"""


@spam_ns.response(404, 'Message not found')
@spam_ns.route('/unflag/<int:id>')
class MessageList(Resource):
    @spam_ns.response(204, 'Message unflagged')
    def post(self, id):
        """Unflag a message (moves it to inbox)"""
        message = spam_model.get(id)

        if not message:
            spam_ns.abort(404, 'Message not found')

        parameters = [
            message.get('name'),
            message.get('email'),
            message.get('subject'),
            message.get('content'),
            message.get('relevance')
        ]

        if message:
            try:
                message_model.create(parameters)
            except Exception as e:
                spam_ns.abort(500, 'An error occurred')
            try:
                spam_model.delete(message.get('id'))
            except Exception as e:
                message_model.delete(message.get('id'))
                spam_ns.abort(500, 'An error occurred')

        return '', 204
