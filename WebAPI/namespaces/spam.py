from flask import request, render_template, make_response
from flask_restx import Namespace, Resource, fields

from MessageTagging.spam_detector import SpamDetector
from WebAPI.utils.mailer import Mailer
from database.models.spam import SpamModel
from database.repository import DbRepository

spam_ns = Namespace('spam', description='Spam operations')

db_repository = DbRepository()
spam_model = SpamModel()
mailer = Mailer()
sd = SpamDetector()

message_read_model = spam_ns.model('Message', {
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

    @spam_ns.doc('get spam')
    @spam_ns.param('query', 'search query')
    @spam_ns.param('sort_by', 'Field to sort the messages by')
    @spam_ns.param('sort_order', 'Order to sort the messages (ASC or DESC)')
    @spam_ns.param('page', 'The page to retrieve')
    @spam_ns.param('page_size', 'The number of messages to retrieve per page')
    @spam_ns.produces(['application/json', 'text/html'])
    def get(self):
        """Get (paginated) spam (HTML or JSON)"""
        args = request.args
        query = args.get('query', '', type=str)
        page = args.get('page', 1, type=int)
        page_size = args.get('page_size', 10, type=int)
        sort_by = args.get('sort_by', 'id')  # Default sort by 'id'
        sort_order = args.get('sort_order', 'ASC').upper()  # Default sort order 'ASC'

        if sort_order not in ['ASC', 'DESC']:
            spam_ns.abort(400, "sort_order must be either 'ASC' or 'DESC'")

        valid_sort_fields = ['id', 'name', 'email', 'subject', 'timestamp', 'relevance', 'content']
        if sort_by not in valid_sort_fields:
            spam_ns.abort(400, f"Invalid sort_by field. Must be one of {valid_sort_fields}")

        messages, total_pages = spam_model.get_page(page, page_size, sort=sort_by, sort_order=sort_order,
                                                       search=query)

        accept_header = request.headers.get('Accept', '')
        if 'text/html' in accept_header:
            response = make_response(render_template('component/messages_template.html', messages=messages))
            response.headers['X-Total-Pages'] = total_pages
            response.headers['X-Current-Page'] = page
            return response
        else:
            return {
                'messages': messages,
                'total_pages': total_pages,
                'current_page': page,
                'page_size': page_size
            }


@spam_ns.route('/<int:id>')
@spam_ns.response(404, 'Message not found')
class Message(Resource):
    @spam_ns.marshal_with(message_read_model)
    def get(self, id):
        return spam_ns.get(id)
        messages_ns.abort(404, "Message not found")


    @spam_ns.response(204, 'Message deleted')
    def delete(self, id):
        """Delete a message by id"""
        spam_ns.delete(id)
        return 'Deleted message', 204
