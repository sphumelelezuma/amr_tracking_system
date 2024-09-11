document.addEventListener('DOMContentLoaded', function() {
    const pathogenSelect = document.getElementById('pathogen-select');
    const locationSelect = document.getElementById('location-select');
    const pathogenInput = document.getElementById('pathogen-input');
    const locationInput = document.getElementById('location-input');
    const menuIcon = document.querySelector('.menu-icon');
    const navLinks = document.querySelector('.nav-links');

    menuIcon.addEventListener('click', function() {
        navLinks.classList.toggle('active');
    });

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    document.getElementById('data-entry-form').addEventListener('submit', function(event) {
        event.preventDefault();

        let formData = new FormData(this);
        const newPathogen = pathogenInput.value.trim();
        const newLocation = locationInput.value.trim();

        // Function to handle new pathogen addition
        function handleNewPathogen() {
            return fetch('/add-pathogen/', {
                method: 'POST',
                body: new FormData(document.getElementById('data-entry-form')),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.id) {
                    pathogenSelect.add(new Option(data.name, data.id));
                    pathogenSelect.value = data.id;
                }
            });
        }

        // Function to handle new location addition
        function handleNewLocation() {
            return fetch('/add-location/', {
                method: 'POST',
                body: new FormData(document.getElementById('data-entry-form')),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.id) {
                    locationSelect.add(new Option(data.name, data.id));
                    locationSelect.value = data.id;
                }
            });
        }

        // Add new pathogen if necessary and then submit data
        const pathogenPromise = newPathogen ? handleNewPathogen() : Promise.resolve();
        const locationPromise = newLocation ? handleNewLocation() : Promise.resolve();

        Promise.all([pathogenPromise, locationPromise]).then(() => {
            // Submit the data
            fetch('/submit-data/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => {
                        throw new Error('Error: ' + text);
                    });
                }
                return response.json();
            })
            .then(data => {
                // Handle successful data submission
                console.log(data);
                // Redirect to Data Review page
                window.location.href = '/data_review/';

            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});
