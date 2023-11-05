from WebInterface.tableBuilder import TableBuilder
from dbrepository import DatabaseRepository


class TableFactory:

    def __init__(self):
        self.db = DatabaseRepository()

    @staticmethod
    def delete_link(row_data):
        return f'<a href="/message/delete/{row_data[0]}" class="delete-icon"><i class="material-icons">delete</i></a>'

    @staticmethod
    def flag_link(row_data):
        return f'<a href="/message/flag/{row_data[0]}" class="flag-icon" title="Flag Message"><i class="material-icons">flag</i></a>'

    def get_message_table(self, page=0, page_size=10):
        headers = [
            ("ID", "70px"),
            ("Sender", "100px"),
            ("Relevance", "100px"),
            ("Message", "ifr"),
            ("", "50px"),
            ("", "50px")
        ]

        messages, total_pages = self.db.get_messages(page, page_size)

        table_data = (TableBuilder()
                      .set_headers(headers)
                      .add_rows(messages)
                      .set_pagination(enabled=True, page_size=page_size)
                      .set_total_pages(total_pages)
                      .set_current_page(page)
                      .set_sortable(["ID"])
                      .set_on_click("/message/{0}")
                      .add_callback_column(self.flag_link)
                      .add_callback_column(self.delete_link)
                      .get_table_data())

        return table_data
