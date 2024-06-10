document.addEventListener('DOMContentLoaded', function() {
    const image = document.getElementById('photo');
    const photoContainer = document.getElementById('photo-container');

    photoContainer.addEventListener('click', function(event) {
        const rect = photoContainer.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        const normalizedX = x / rect.width;
        const normalizedY = y / rect.height;

        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')  // Update CSRF token handling
            },
            body: `x=${normalizedX}&y=${normalizedY}`
        }).then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                const pin = document.createElement('div');
                pin.className = 'pin';
                pin.style.left = `${normalizedX * 100}%`;
                pin.style.top = `${normalizedY * 100}%`;
                photoContainer.appendChild(pin);
            }
        });
    });
});

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
