// JavaScript for returning books
        const returnForm = document.getElementById('return-form');
        const returnStatus = document.getElementById('return-status');
        
        returnForm.addEventListener('submit', function (e) {
            e.preventDefault();
            
            // Retrieve member username and book ISBN
            const username = document.getElementById('username').value;
            const isbn = document.getElementById('isbn').value;
            
            // Construct the URL for returning a book
            const url = `/return_books/?username=${username}&isbn=${isbn}`;
            
            // Send a POST request to return the book
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    returnStatus.innerHTML = `Book with ISBN ${isbn} has been returned by ${username}.`;
                    // Optionally, you can clear the form here
                    returnForm.reset();
                } else {
                    returnStatus.innerHTML = `Error: ${data.message}`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });