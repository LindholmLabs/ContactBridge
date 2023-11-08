// Function to fetch data and update the table
function fetchData(endpoint, queryParams) {
    const url = new URL(endpoint, window.location.origin);
    Object.keys(queryParams).forEach(key => url.searchParams.append(key, queryParams[key]));

    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.setRequestHeader('Accept', 'text/html');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById('table-body').innerHTML = xhr.responseText;
            const totalPages = xhr.getResponseHeader('X-total-pages');
            const currentPage = xhr.getResponseHeader('X-current-page');
            updatePagination(parseInt(currentPage, 10), parseInt(totalPages, 10), queryParams.page_size, endpoint);
        }
    };
    xhr.send();
}

// handle search input for messages or users
function searchData() {
    const searchInput = document.getElementById('search-bar').value;
    const pageSize = document.getElementById('page-size').value;
    const queryParams = {
        query: searchInput,
        page_size: pageSize
    };
    fetchData(API_ENDPOINT, queryParams);
}

// Function to update pagination
function updatePagination(currentPage, totalPages, pageSize) {
    const container = document.getElementById('pagination-container');
    container.innerHTML = ''; // Clear existing pagination

    // Create the 'Back' button
    const backLi = document.createElement('li');
    backLi.className = currentPage === 1 ? 'disabled' : 'waves-effect';
    const backA = document.createElement('a');
    backA.href = '#!';
    backA.innerHTML = '&laquo;';
    backA.onclick = function() {
        if (currentPage > 1) {
            fetchData(API_ENDPOINT, { page: currentPage - 1, page_size: pageSize });
        }
    };
    backLi.appendChild(backA);
    container.appendChild(backLi);

    // Create the page number buttons
    for (let i = 1; i <= totalPages; i++) {
        const li = document.createElement('li');
        li.className = i === currentPage ? 'active' : 'waves-effect';
        const a = document.createElement('a');
        a.href = '#!';
        a.textContent = i;
        a.onclick = function() {
            fetchData(API_ENDPOINT, { page: i, page_size: pageSize });
        };
        li.appendChild(a);
        container.appendChild(li);
    }

    // Create the 'Forward' button
    const forwardLi = document.createElement('li');
    forwardLi.className = currentPage === totalPages ? 'disabled' : 'waves-effect';
    const forwardA = document.createElement('a');
    forwardA.href = '#!';
    forwardA.innerHTML = '&raquo;';
    forwardA.onclick = function() {
        if (currentPage < totalPages) {
            fetchData(API_ENDPOINT, { page: currentPage + 1, page_size: pageSize });
        }
    };
    forwardLi.appendChild(forwardA);
    container.appendChild(forwardLi);
}

// Function to sort table by clicking on headers
function sortTableByHeader(type) {
    document.querySelectorAll('#table-headers th').forEach(header => {
        header.addEventListener('click', () => {
            const sortField = header.getAttribute('data-field');
            const sortOrder = header.getAttribute('data-order');
            const searchInput = document.getElementById('search-bar').value;
            const pageSize = document.getElementById('page-size').value || 10;
            const queryParams = {
                query: searchInput,
                sort_by: sortField,
                sort_order: sortOrder,
                page_size: pageSize
            };
            fetchData(`/api/${type}`, queryParams);
            // Toggle sort order for the next click
            header.setAttribute('data-order', sortOrder === 'asc' ? 'desc' : 'asc');
        });
    });
}

// Initial fetch for messages and setup headers sorting
document.addEventListener('DOMContentLoaded', function() {
    M.AutoInit();  // Initialize all Materialize components
    fetchData(API_ENDPOINT, { page: 1, page_size: 10 });
    sortTableByHeader('messages');
});