const issueForm = document.getElementById('issue-form');
        const issueButton = document.getElementById('issue-button');
        const messageContainer = document.getElementById('message-container');

        issueButton.addEventListener('click', function () {
            const username = document.getElementById('username').value;
            const isbn = document.getElementById('isbn').value;

            if (!isValidUsername(username) || !isValidISBN(isbn)) {
                alert('Please enter valid member username and book ISBN.');
            } else {
                sendIssueRequest(username, isbn);
            }
        });

        function isValidUsername(username) {
            const usernameRegex = /^[a-zA-Z0-9_-]{3,20}$/;
            return usernameRegex.test(username);
        }

        function isValidISBN(isbn) {
            const isbnRegex = /^(?:\d{10}|\d{13})$/;
            return isbnRegex.test(isbn);
        }

        function sendIssueRequest(username, isbn) {
            const requestData = {
                username: username,
                isbn: isbn,
            };

            fetch('{% url "issue_books" %}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify(requestData),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Book issuing was successful
                    showMessage('success', 'Book issued successfully.');
                    // Optionally, you can perform additional actions here.
                } else {
                    // Book issuing failed
                    showMessage('error', 'Book issuing failed.');
                    // Optionally, display an error message or take other actions.
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('error', 'An error occurred while processing your request.');
            });
        }

        function showMessage(type, text) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add(type);
            messageDiv.textContent = text;
            messageContainer.innerHTML = '';
            messageContainer.appendChild(messageDiv);
        }

        // Helper function to get the CSRF token from cookies
        function getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        }