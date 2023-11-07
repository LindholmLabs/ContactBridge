import math

from database.repository import DbRepository


class MessageModel:
    def __init__(self):
        self.db_repository = DbRepository()

    def get_page(self, page, page_size, sort="id", sort_order="ASC"):
        total_messages_query = 'SELECT COUNT(*) FROM messages'
        total_messages = self.db_repository.execute_query(total_messages_query, expect_result=True)[0][0]

        offset = (page - 1) * page_size
        total_pages = math.ceil(total_messages / page_size)

        paginated_messages_query = f"""
            SELECT id, name, email, subject, content, timestamp, relevance 
            FROM messages
            ORDER BY {sort} {sort_order} 
            LIMIT ? OFFSET ?
        """

        paginated_messages = self.db_repository.execute_query(
            paginated_messages_query,
            (page_size, offset),
            expect_result=True
        )

        labeled_messages = [
            {
                'id': message[0],
                'name': message[1],
                'email': message[2],
                'subject': message[3],
                'content': message[4],
                'timestamp': message[5],
                'relevance': message[6]
            }
            for message in paginated_messages
        ]

        return labeled_messages, total_pages

    def get(self, message_id):
        query = 'SELECT * FROM messages WHERE id = ?'
        result = self.db_repository.execute_query(query, (message_id,), expect_result=True)
        return result[0] if result else None

    def create(self, parameters):
        create_query = """
            INSERT INTO messages (name, email, subject, content, relevance) 
            VALUES (?, ?, ?, ?, ?)
        """
        self.db_repository.execute_query(create_query, parameters)

    def update(self, parameters):
        update_query = """
            UPDATE messages
            SET name = ?, email = ?, subject = ?, content = ?, relevance = ?
            WHERE id = ?
        """
        self.db_repository.execute_query(update_query, parameters)
