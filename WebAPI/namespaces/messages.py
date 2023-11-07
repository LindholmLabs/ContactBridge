from flask import request
from flask_restx import Namespace, Resource, fields

from database.models.messages import MessageModel
from database.repository import DbRepository

messages_ns = Namespace('messages', description='Message operations')

db_repository = DbRepository()
message_model = MessageModel()

message_read_model = messages_ns.model('Message', {
    'id': fields.Integer(readOnly=True, description='The message unique identifier'),
    'name': fields.String(required=True, description='The senders name'),
    'email': fields.String(required=True, description='The email address of the sender'),
    'subject': fields.String(required=False, description='The subject of the message'),
    'content': fields.String(required=True, description='The content of the message'),
    'timestamp': fields.String(required=True, description='The time at which the message was sent'),
    'relevance': fields.Float(readOnly=True, description='relevance, tries to set to low values for spam')
})

message_create_model = messages_ns.model('Message', {
    'name': fields.String(required=True, description='The senders name'),
    'email': fields.String(required=True, description='The email address of the sender'),
    'content': fields.String(required=True, description='The content of the message'),
})

paginated_message_model = messages_ns.model('MessageList', {
    'messages': fields.List(fields.Nested(message_read_model), description='List of message objects'),
    'total_pages': fields.Integer(description='Total number of pages'),
    'current_page': fields.Integer(description='The current page'),
    'page_size': fields.Integer(description='The number of messages per page')
})


@messages_ns.route('/')
class MessageList(Resource):

    @messages_ns.param('sort_by', 'Field to sort the messages by')
    @messages_ns.param('sort_order', 'Order to sort the messages (ASC or DESC)')
    @messages_ns.param('page', 'The page to retrieve')
    @messages_ns.param('page_size', 'The number of messages to retrieve per page')
    @messages_ns.marshal_list_with(paginated_message_model)
    def get(self):
        args = request.args
        page = args.get('page', 1, type=int)
        page_size = args.get('page_size', 10, type=int)
        sort_by = args.get('sort_by', 'id')  # Default sort by 'id'
        sort_order = args.get('sort_order', 'ASC').upper()  # Default sort order 'ASC'

        if sort_order not in ['ASC', 'DESC']:
            messages_ns.abort(400, "sort_order must be either 'ASC' or 'DESC'")

        valid_sort_fields = ['id', 'name', 'email', 'subject', 'timestamp', 'relevance']
        if sort_by not in valid_sort_fields:
            messages_ns.abort(400, f"Invalid sort_by field. Must be one of {valid_sort_fields}")

        messages, total_pages = message_model.get_page(page, page_size, sort=sort_by, sort_order=sort_order)

        return {
            'messages': messages,
            'total_pages': total_pages,
            'current_page': page,
            'page_size': page_size
        }

    # Create message
    @messages_ns.expect(message_create_model)
    def post(self):
        data = request.json
        query = "INSERT INTO messages (name, email, content) VALUES (?, ?, ?)"
        db_repository.execute_query(query, (data['name'], data['email'], data['content']))
        return {'message': 'Message saved successfully'}, 201


@messages_ns.route('/<int:id>')
@messages_ns.response(404, 'Message not found')
class Message(Resource):
    @messages_ns.marshal_with(message_read_model)
    def get(self, id):
        query = "SELECT * FROM messages WHERE id = ?"
        message = db_repository.execute_query(query, (id,), expect_result=True)
        if message:
            return message[0]
        messages_ns.abort(404, "Message not found")

    @messages_ns.expect(message_read_model)
    def put(self, id):
        """Update a message given its ID"""
        data = request.json
        query = "UPDATE messages SET email = ?, content = ? WHERE id = ?"
        db_repository.execute_query(query, (data['email'], data['content'], id))
        return {'message': 'Message updated successfully'}, 200