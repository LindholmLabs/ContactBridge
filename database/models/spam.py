import math

from database.repository import DbRepository


class SpamModel:
    def __init__(self):
        self.db_repository = DbRepository()

    def get_page(self, page, page_size, sort="id", sort_order="ASC", search=''):
        search_term = f"%{search}%"

        common_sql_query_base = f"""
               FROM spam
               WHERE (name LIKE ? OR email LIKE ? OR subject LIKE ? OR content LIKE ?)
           """

        total_messages_query = f"""
            SELECT COUNT(*)
            {common_sql_query_base}
        """

        total_messages = self.db_repository.execute_query(
            total_messages_query,
            (search_term, search_term, search_term, search_term),
            expect_result=True
        )

        total_messages_count = total_messages[0][0] if total_messages else 0
        offset = (page - 1) * page_size
        total_pages = math.ceil(total_messages_count / page_size)

        paginated_messages_query = f"""
                SELECT id, name, email, subject, content, timestamp, relevance
                {common_sql_query_base}
                ORDER BY {sort} {sort_order} 
                LIMIT ? OFFSET ?
            """

        paginated_messages = self.db_repository.execute_query(
            paginated_messages_query,
            (search_term, search_term, search_term, search_term, page_size, offset),
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
        query = 'SELECT * FROM spam WHERE id = ?'
        result = self.db_repository.execute_query(query, (message_id,), expect_result=True)

        if result:
            message = result[0]
            labeled_message = {
                    'id': message[0],
                    'name': message[1],
                    'email': message[2],
                    'subject': message[3],
                    'content': message[4],
                    'timestamp': message[5],
                    'relevance': message[6]
                }
            return labeled_message

        return None

    def create(self, parameters):
        create_query = """
            INSERT INTO spam (name, email, subject, content, relevance) 
            VALUES (?, ?, ?, ?, ?)
        """
        self.db_repository.execute_query(create_query, parameters)

    def update(self, parameters):
        update_query = """
            UPDATE spam
            SET name = ?, email = ?, subject = ?, content = ?, relevance = ?
            WHERE id = ?
        """
        self.db_repository.execute_query(update_query, parameters)

    def delete(self, message_id):
        delete_query = "DELETE FROM spam WHERE id = ?"
        self.db_repository.execute_query(delete_query, (message_id,))
