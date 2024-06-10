document.addEventListener("DOMContentLoaded", function() {
    const img = document.getElementById('photo');
    img.onload = function() {
        const pins = document.querySelectorAll('.pin-c');
        const imgWidth = img.offsetWidth;
        const imgHeight = img.offsetHeight;

        pins.forEach(pin => {
            const x = pin.getAttribute('data-x');
            const y = pin.getAttribute('data-y');

            pin.style.left = x + '%';
            pin.style.top = y + '%';
        });
    };
});
