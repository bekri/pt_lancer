window.onload = function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
};

function showPosition(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    const apiKey = 'pk.0addd0bd47c1b87af45d10fb3b907986'; // Replace with your LocationIQ API key
    
    // Make a request to the LocationIQ Geocoding API
    fetch(`https://us1.locationiq.com/v1/reverse.php?key=${apiKey}&lat=${latitude}&lon=${longitude}&format=json`)
        .then(response => response.json())
        .then(data => {
            const city = data.address.city;
            const country = data.address.country;
            // Display longitude, latitude, city, and country separately
            document.getElementById('longitude').textContent = longitude;
            document.getElementById('latitude').textContent = latitude;
            document.getElementById('city').textContent = city;
            document.getElementById('country').textContent = country;

            // Send location data to backend for saving
            sendLocationDataToBackend(latitude, longitude, city, country);
        })
        .catch(error => {
            console.error('Error fetching geocode data:', error);
        });
}

function sendLocationDataToBackend(latitude, longitude, city, country) {
    // Make AJAX request to send location data to backend only if data is retrieved successfully
    if (latitude && longitude && city && country) {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/update-location/', true); // Specify the URL of the Django view
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ latitude, longitude, city, country }));
    }
}

function showError(error) {
    console.error('Error getting geolocation:', error);
}



// This function sends the location data to the Django backend for saving
function saveLocationDataToBackend() {
    // Extract the longitude, latitude, city, and country from the HTML elements
    const longitude = document.getElementById('longitude').textContent;
    const latitude = document.getElementById('latitude').textContent;
    const city = document.getElementById('city').textContent;
    const country = document.getElementById('country').textContent;

    // Make an AJAX request to send location data to backend for saving
    fetch('/save-location/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token in headers
        },
        body: JSON.stringify({ latitude, longitude, city, country })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); // Log the response from the backend
    })
    .catch(error => {
        console.error('Error saving location data:', error);
    });
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Search for CSRF token
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Call the function to save location data to the backend when the page loads
saveLocationDataToBackend();
