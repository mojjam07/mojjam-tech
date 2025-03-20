document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#contact form');
    console.log(document); // Log the entire document to check if the form is present
    console.log(form); // Log the form element to check if it is selected correctly
    
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Simple form validation
        const name = form.querySelector('input[type="text"]').value;
        const email = form.querySelector('input[type="email"]').value;
        const message = form.querySelector('textarea').value;

        if (name === '' || email === '' || message === '') {
            alert('Please fill in all fields.');
            return;
        }

        // If validation passes, send data to the backend
        fetch('/contact/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, message }),
        })
        .then(response => {
            if (response.ok) {
                alert('Form submitted successfully!');
                form.reset();
            } else {
                alert('There was a problem with your submission.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was a problem with your submission.');
        });
    });
});
