var currentPage;
var totalPages;

document.addEventListener('DOMContentLoaded', function () {
  var paginationElement = document.querySelector('.pagination');
  if (paginationElement) {
    currentPage = parseInt(paginationElement.getAttribute('data-current-page'), 10);
    totalPages = parseInt(paginationElement.getAttribute('data-total-pages'), 10);
  }
});

function changePage(direction) {
    if (typeof currentPage === 'undefined' || typeof totalPages === 'undefined') {
        console.error('currentPage or totalPages is undefined');
        return;
    }

    var newPage = currentPage;
    if (direction === 'next' && currentPage < totalPages) {
        newPage = currentPage + 1;
    } else if (direction === 'prev' && currentPage > 1) {
        newPage = currentPage - 1;
    }

    window.location.href = '?page=' + newPage;
}