document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contact-form');
    
    if (!form) {
        console.warn('Contact form not found');
        return;
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'), 
            message: formData.get('message')
        };

        if (!data.name || !data.email || !data.message) {
            alert('Please fill in all fields.');
            return;
        }

        fetch(form.action || '/contact/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (response.ok) {
                alert('Form submitted successfully!');
                form.reset();
            } else {
                throw new Error('Network response was not ok');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was a problem with your submission.');
        });
    });
});
