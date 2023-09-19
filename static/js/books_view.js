const searchForm = document.getElementById('search-form');
const bookList = document.getElementById('book-list');

searchForm.addEventListener('submit', function (e) {
    e.preventDefault();

    // Retrieve search criteria
    const title = document.getElementById('title').value;
    const authors = document.getElementById('authors').value;

    // Construct the URL for fetching book data based on search criteria
    const url = `/get_books/?title=${title}&authors=${authors}`;

    // Fetch book data from the server
    fetch(url)
        .then(response => response.text())
        .then(data => {
            // Update the book list with the retrieved data
            bookList.innerHTML = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
});