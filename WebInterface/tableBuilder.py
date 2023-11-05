class TableInstance:
    def __init__(self):
        self.headers = []
        self.rows = []
        self.sortable_columns = []
        self.pagination_enabled = False
        self.page_size = 10
        self.current_page = 1
        self.callback_column = None
        self.row_click_url_template = ""

    def add_header(self, header):
        self.headers.append(header)

    def add_row(self, row):
        self.rows.append(row)

    def enable_pagination(self, page_size=10):
        self.pagination_enabled = True
        self.page_size = page_size

    def set_sortable_columns(self, columns):
        self.sortable_columns = columns

    def set_callback_column(self, callback):
        self.callback_column = callback

    def set_row_click_url_template(self, url_template):
        self.row_click_url_template = url_template


class TableBuilder:
    def __init__(self):
        self.table_instance = TableInstance()

    def set_headers(self, headers):
        for header in headers:
            self.table_instance.add_header(header)

    def add_rows(self, rows):
        for row in rows:
            self.table_instance.add_row(row)

    def set_pagination(self, enabled=True, page_size=10):
        if enabled:
            self.table_instance.enable_pagination(page_size)

    def set_sortable(self, sortable_columns):
        self.table_instance.set_sortable_columns(sortable_columns)

    def add_callback_column(self, callback):
        self.table_instance.set_callback_column(callback)

    def set_on_click(self, url_template):
        self.table_instance.set_row_click_url_template(url_template)

    def build(self):
        return self.table_instance