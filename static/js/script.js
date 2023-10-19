document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const summaryResult = document.getElementById('summary-result');
    const loadingDiv = document.getElementById('loading');

    // Handle file upload form submission
    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault();
        loadingDiv.style.display = 'block';
        
        const formData = new FormData(uploadForm);
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            summaryResult.style.display = 'block';
            summaryResult.innerHTML = `<strong>Summary:</strong> ${data.summary}`;
            loadingDiv.style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            summaryResult.style.display = 'block';
            summaryResult.innerHTML = 'Error generating summary. Please try again later.';
            loadingDiv.style.display = 'none';
        });
    });
});

// New function to handle switch
// If on, tell app.py to set APP_MODE to "advanced"
// If off, tell app.py to set APP_MODE to "simple"


// Get the switch checkbox element
const modeSwitch = document.querySelector('.switch input[type="checkbox"]');

// Add event listener for change
modeSwitch.addEventListener('change', function() {
    // Determine the mode based on checkbox status
    const mode = this.checked ? 'advanced' : 'simple';

    // Make a POST request to /set-mode in app.py with the mode as data
    fetch('/set-mode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mode: mode })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Mode set:', data.message);
    })
    .catch(error => {
        console.error('Error setting mode:', error);
    });
});

// Get the mode description element
const modeDescription = document.getElementById('mode-description');

// Update the mode description based on the switch status
function updateModeDescription() {
    modeDescription.textContent = (modeSwitch.checked ? "Advanced" : "Simple");
}

// Call the function initially to set the correct mode description
updateModeDescription();

// Also call the function when the switch status changes
modeSwitch.addEventListener('change', updateModeDescription);
