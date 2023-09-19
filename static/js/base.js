document.addEventListener('DOMContentLoaded', function () {
    const navLinks = document.querySelectorAll('nav ul li a');

    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {

            const url = this.getAttribute('href'); // Use the href attribute
            document.querySelector('main').innerHTML = '<p>Loading...</p>';
        });
    });
});
