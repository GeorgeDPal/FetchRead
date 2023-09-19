const memberForm = document.getElementById('member-form');
        const usernameInput = document.getElementById('username');
        const emailInput = document.getElementById('email');
        const usernameError = document.getElementById('username-error');
        const emailError = document.getElementById('email-error');
        const submitButton = document.getElementById('submit-button');

        // Function to check if a username is already taken
        async function isUsernameTaken(username) {
            const response = await fetch(`{% url 'check_username' %}?username=${username}`);
            const data = await response.json();
            return data.taken;
        }

        // Function to check if an email is already registered
        async function isEmailRegistered(email) {
            const response = await fetch(`{% url 'check_email' %}?email=${email}`);
            const data = await response.json();
            return data.registered;
        }

        // Function to handle username validation
        async function validateUsername() {
            const username = usernameInput.value.trim();
            if (username === '') {
                usernameError.textContent = 'Username is required.';
                return false;
            }
            
            if (await isUsernameTaken(username)) {
                usernameError.textContent = 'Username is already taken.';
                return false;
            }

            usernameError.textContent = '';
            return true;
        }

        // Function to handle email validation
        async function validateEmail() {
            const email = emailInput.value.trim();
            if (email === '') {
                emailError.textContent = 'Email is required.';
                return false;
            }

            if (await isEmailRegistered(email)) {
                emailError.textContent = 'Email is already registered.';
                return false;
            }

            emailError.textContent = '';
            return true;
        }

        // Function to handle form submission
        memberForm.addEventListener('submit', async function (e) {
            const isUsernameValid = await validateUsername();
            const isEmailValid = await validateEmail();

            if (!isUsernameValid || !isEmailValid) {
                e.preventDefault();
                return;
            }
        });