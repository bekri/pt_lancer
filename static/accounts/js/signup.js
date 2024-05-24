// static/accounts/js/signup.js
document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form submission

    // Perform form submission using fetch API
    fetch(this.action, {
        method: this.method,
        body: new FormData(this)
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '{% url 'verify' %}';  // Redirect to verification page
        } else {
            // Handle error responses
        }
    })
    .catch(error => {
        // Handle fetch errors
    });
});
