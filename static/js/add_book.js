document.addEventListener('DOMContentLoaded', function () {
    const addBookForm = document.getElementById('addBookForm');
    const message = document.getElementById('message');

    addBookForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(addBookForm);

        fetch('{% url 'add_book' %}', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                message.innerHTML = 'Book added successfully.';
                addBookForm.reset();  // Clear the form
            } else {
                message.innerHTML = 'Error: ' + data.message;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});