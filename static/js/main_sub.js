const subjectsItemsPerPage = 3;
let currentSubjectsPage = 0;

function showSubjectsPage(page) {
    const subjects = document.querySelectorAll('#subjects-container .subject-card');
    const totalSubjectsItems = subjects.length;
    const totalSubjectsPages = Math.ceil(totalSubjectsItems / subjectsItemsPerPage);

    if (page < 0) page = 0;
    if (page >= totalSubjectsPages) page = totalSubjectsPages - 1;

    subjects.forEach((card, index) => {
        card.style.display = (index >= page * subjectsItemsPerPage && index < (page + 1) * subjectsItemsPerPage) ? 'block' : 'none';
    });

    currentSubjectsPage = page;

    document.getElementById('subjects-prev-btn').disabled = (currentSubjectsPage <= 0);
    document.getElementById('subjects-next-btn').disabled = (currentSubjectsPage >= totalSubjectsPages - 1);
}

function prevSubjectsPage() {
    showSubjectsPage(currentSubjectsPage - 1);
}

function nextSubjectsPage() {
    showSubjectsPage(currentSubjectsPage + 1);
}

document.addEventListener('DOMContentLoaded', () => {
    showSubjectsPage(currentSubjectsPage);
});