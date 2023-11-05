class TableBuilder:
    def __init__(self):
        self.headers = []
        self.rows = []
        self.sortable_columns = []
        self.pagination_enabled = False
        self.page_size = 10
        self.current_page = 1
        self.total_pages = 0
        self.callback_columns = []
        self.row_click_url_template = ""

    def add_header(self, header):
        self.headers.append(header)
        return self

    def add_row(self, row):
        self.rows.append(row)
        return self

    def enable_pagination(self, page_size=10):
        self.pagination_enabled = True
        self.page_size = page_size
        return self

    def set_sortable_columns(self, columns):
        self.sortable_columns = columns
        return self

    def set_callback_column(self, callback):
        self.callback_column = callback
        return self

    def set_row_click_url_template(self, url_template):
        self.row_click_url_template = url_template
        return self

    def set_headers(self, headers):
        for header in headers:
            self.add_header(header)
        return self

    def add_rows(self, rows):
        for row in rows:
            self.add_row(row)
        return self

    def set_pagination(self, enabled=True, page_size=10):
        if enabled:
            self.enable_pagination(page_size)
        return self

    def set_total_pages(self, total_pages):
        self.total_pages = total_pages
        return self

    def set_current_page(self, page):
        self.current_page = page
        return self

    def set_sortable(self, sortable_columns):
        self.set_sortable_columns(sortable_columns)
        return self

    def add_callback_column(self, callback):
        self.callback_columns.append(callback)
        return self

    def set_on_click(self, url_template):
        self.set_row_click_url_template(url_template)
        return self

    def get_table_data(self):
        return {
            "headers": self.headers,
            "rows": self.rows,
            "sortable_columns": self.sortable_columns,
            "pagination_enabled": self.pagination_enabled,
            "page_size": self.page_size,
            "current_page": self.current_page,
            "total_pages": self.total_pages,
            "callback_columns": self.callback_columns,
            "row_click_url_template": self.row_click_url_template
        }
