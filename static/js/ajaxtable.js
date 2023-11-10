class AjaxTable {
    constructor(apiEndpoint, tableHeadersId, tableBodyId, searchBarId, pageSizeSelectorId, paginationContainerId) {
        this.apiEndpoint = apiEndpoint;
        this.tableHeadersId = tableHeadersId;
        this.tableBodyId = tableBodyId;
        this.searchBarId = searchBarId;
        this.pageSizeSelectorId = pageSizeSelectorId;
        this.paginationContainerId = paginationContainerId;

        this.currentPage = 1;
        this.currentPageSize = 10; // Default page size
        this.currentSearchQuery = '';
        this.currentSortField = null;
        this.currentSortOrder = null;

        this.initEventListeners();
        this.fetchData({ page: 1, page_size: 10 });
    }

    initEventListeners() {
        const debouncedSearchData = this.debounce(this.searchData.bind(this), 500);
        document.getElementById(this.searchBarId).addEventListener('keyup', debouncedSearchData);

        document.getElementById(this.pageSizeSelectorId).addEventListener('change', () => {
            this.currentPageSize = document.getElementById(this.pageSizeSelectorId).value;
            this.currentPage = 1; // Reset to first page on page size change
            this.fetchData();
        });

        document.addEventListener('htmx:afterRequest', (evt) => {
            this.fetchData();
        });

        document.getElementById(this.tableBodyId).addEventListener('click', event => {
            if (event.target.classList.contains('delete-button')) {
                const itemId = event.target.dataset.itemId;
                this.confirmDelete(this.apiEndpoint, itemId);
            }
        });

        this.sortTableByHeader();
    }

    confirmDelete(apiEndpoint, itemId) {
        const deleteButton = document.getElementById('confirmDeleteButton');
        deleteButton.onclick = () => this.performDeletion(apiEndpoint, itemId);

        // Open confirmation modal
        var instance = M.Modal.getInstance(document.getElementById('deleteConfirmationModal'));
        instance.open();
    }

    performDeletion(apiEndpoint, itemId) {
        const deleteUrl = `${apiEndpoint}/${itemId}`;

        fetch(deleteUrl, { method: 'DELETE' })
            .then(response => {
                if(response.ok) {
                    this.handleDeletionSuccess(itemId);
                } else {
                    console.error('Deletion failed');
                }
            })
            .catch(error => console.error('Error:', error));
    }

    handleDeletionSuccess(itemId) {
        const rowToRemove = document.getElementById('itemRow-' + itemId);
        if (rowToRemove) {
            rowToRemove.remove();
        } else {
            this.fetchData(); // Refresh the table data
        }
    }

    // Function to fetch data and update the table
    fetchData() {
        const queryParams = {
            page: this.currentPage,
            page_size: this.currentPageSize,
            query: this.currentSearchQuery
        };

        if (this.currentSortField && this.currentSortOrder) {
            queryParams.sort_by = this.currentSortField;
            queryParams.sort_order = this.currentSortOrder;
        }

        const url = new URL(this.apiEndpoint, window.location.origin);
        Object.keys(queryParams).forEach(key => url.searchParams.append(key, queryParams[key]));

        fetch(url, { headers: { 'Accept': 'text/html' } })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                // Extract custom headers before processing the text
                const totalPages = response.headers.get('X-total-pages');
                const currentPage = response.headers.get('X-current-page');
                this.updatePagination(parseInt(totalPages, 10));

                return response.text();
            })
            .then(html => {
                const tableBody = document.getElementById(this.tableBodyId);
                tableBody.innerHTML = html;
                htmx.process(tableBody); // Reinitialize htmx for new content
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
    }

    updatePagination(totalPages) {
        console.log(totalPages)
        const container = document.getElementById(this.paginationContainerId);
        container.innerHTML = '';

        // Create back button
        const createBackButton = () => {
            const li = document.createElement('li');
            li.className = this.currentPage === 1 ? 'disabled' : 'waves-effect';
            const a = document.createElement('a');
            const icon = document.createElement('i');
            icon.className = 'material-icons';
            icon.textContent = 'chevron_left';
            a.appendChild(icon);
            a.onclick = () => {
                if (this.currentPage > 1) {
                    this.currentPage -= 1;
                    this.fetchData({ page: this.currentPage - 1, page_size: this.currentPageSize });
                }
            };
            li.appendChild(a);
            return li;
        };
        container.appendChild(createBackButton());

        // Create page buttons
        for (let i = 1; i <= totalPages; i++) {
            const li = document.createElement('li');
            li.className = i === this.currentPage ? 'active' : 'waves-effect';
            const a = document.createElement('a');
            a.textContent = i;
            a.onclick = () => {
                this.currentPage = i;
                this.fetchData({ page: i, page_size: this.currentPageSize });
            };
            li.appendChild(a);
            container.appendChild(li);
        }

        // Create forward button
        const createForwardButton = () => {
            const li = document.createElement('li');
            li.className = this.currentPage === totalPages ? 'disabled' : 'waves-effect';
            const a = document.createElement('a');
            const icon = document.createElement('i');
            icon.className = 'material-icons';
            icon.textContent = 'chevron_right';
            a.appendChild(icon);
            a.onclick = () => {
                if (this.currentPage < totalPages) {
                    this.currentPage += 1;
                    this.fetchData({ page: this.currentPage + 1, page_size: this.currentPageSize });
                }
            };
            li.appendChild(a);
            return li;
        };
        container.appendChild(createForwardButton());
    }

    debounce(func, delay) {
        let debounceTimer;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => func.apply(context, args), delay);
        };
    }

    searchData() {
        this.currentSearchQuery = document.getElementById(this.searchBarId).value;
        this.fetchData();
    }

    sortTableByHeader() {
        document.querySelectorAll(`#${this.tableHeadersId} th`).forEach(header => {
            header.addEventListener('click', () => {
                this.currentSortField = header.getAttribute('data-field');
                this.currentSortOrder = header.getAttribute('data-order') === 'asc' ? 'desc' : 'asc';
                header.setAttribute('data-order', this.currentSortOrder);
                this.fetchData();
            });
        });
    }
}