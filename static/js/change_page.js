const subjectsItemsPerPage = 3;
let currentSubjectsPage = 0;
const notesItemsPerPage = 3;
let currentNotesPage = 0;
let itemsPerPage = 2;
let currentPage = 0;
function inititemPerPage(userType) {
    itemsPerPage = (userType >= 1) ? 3 : 2;
}

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


function showNotesPage(page) {
    const notes = document.querySelectorAll('#notes-container .note-card');
    const totalNotesItems = notes.length;
    const totalNotesPages = Math.ceil(totalNotesItems / notesItemsPerPage);

    if (page < 0) page = 0;
    if (page >= totalNotesPages) page = totalNotesPages - 1;

    notes.forEach((card, index) => {
        card.style.display = (index >= page * notesItemsPerPage && index < (page + 1) * notesItemsPerPage) ? 'block' : 'none';
    });

    currentNotesPage = page;

    document.getElementById('notes-prev-btn').disabled = (currentNotesPage <= 0);
    document.getElementById('notes-next-btn').disabled = (currentNotesPage >= totalNotesPages - 1);
}

function prevNotesPage() {
    showNotesPage(currentNotesPage - 1);
}

function nextNotesPage() {
    showNotesPage(currentNotesPage + 1);
}

document.addEventListener('DOMContentLoaded', () => {
    showNotesPage(currentNotesPage);
});

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