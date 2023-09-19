 // JavaScript for displaying a list of books
 const bookList = document.getElementById('book-list');
        
 // Function to fetch and display books
 function fetchAndDisplayBooks() {
     // Fetch the list of books from the server
     fetch('/get_books/')
         .then(response => response.text())
         .then(data => {
             // Update the book list with the retrieved data
             bookList.innerHTML = data;
         })
         .catch(error => {
             console.error('Error:', error);
         });
 }

 // Call the fetchAndDisplayBooks function to initially load the books
 fetchAndDisplayBooks();

 // Add event listener to the search form
 const searchForm = document.getElementById('search-form');
 searchForm.addEventListener('submit', function (e) {
     e.preventDefault();
     
     // Retrieve search criteria
     const title = document.getElementById('title').value;
     const authors = document.getElementById('authors').value;
     
     // Construct the URL for fetching book data based on search criteria
     const url = `/get_books/?title=${title}&authors=${authors}`;
     
     // Fetch and display books based on search criteria
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