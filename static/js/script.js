
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
