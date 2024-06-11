const itemsPerPage = 2;
let currentPage = 0;

function showPage(page) {
    const absences = document.querySelectorAll('#absences-container .absence-card');
    const totalItems = absences.length;
    const totalPages = Math.ceil(totalItems / itemsPerPage);

    if (page < 0) page = 0;
    if (page >= totalPages) page = totalPages - 1;

    absences.forEach((card, index) => {
        card.style.display = (index >= page * itemsPerPage && index < (page + 1) * itemsPerPage) ? 'block' : 'none';
    });

    currentPage = page;

    document.getElementById('prev-btn').disabled = (currentPage <= 0);
    document.getElementById('next-btn').disabled = (currentPage >= totalPages - 1);
}

function prevPage() {
    showPage(currentPage - 1);
}

function nextPage() {
    showPage(currentPage + 1);
}

document.addEventListener('DOMContentLoaded', () => {
    showPage(currentPage);
});