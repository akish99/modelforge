document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const imagePreview = document.getElementById('image-preview');
    const predictBtn = document.getElementById('predict-btn');
    const resultDiv = document.getElementById('result');
    const loader = document.getElementById('loader');
    
    // const API_ENDPOINT = 'http://127.0.0.1:5000/predict';
    const API_ENDPOINT = 'https://modelforge-backend1.onrender.com';

    let uploadedFile = null;

    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            uploadedFile = file;
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.innerHTML = `<img src="${e.target.result}" alt="Image preview"/>`;
            };
            reader.readAsDataURL(file);
            predictBtn.disabled = false;
            resultDiv.innerHTML = '';
        }
    });

    predictBtn.addEventListener('click', () => {
        if (!uploadedFile) {
            alert('Please select an image first!');
            return;
        }

        const formData = new FormData();
        formData.append('file', uploadedFile);

        loader.style.display = 'block';
        resultDiv.style.display = 'none';
        predictBtn.disabled = true;

        fetch(API_ENDPOINT, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                // Try to get a more detailed error from the server's JSON response
                return response.json().then(errorData => {
                    throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.error}`);
                });
            }
            return response.json();
        })
        .then(data => {
            displayResult(data);
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerHTML = `<p style="color: red;">An error occurred: ${error.message}. Please check the backend server terminal for details.</p>`;
        })
        .finally(() => {
            loader.style.display = 'none';
            resultDiv.style.display = 'block';
            predictBtn.disabled = false;
        });
    });

    function displayResult(data) {
        if (data.error) {
            resultDiv.innerHTML = `<p style="color: red;">Error from server: ${data.error}</p>`;
            return;
        }

        // --- UPDATED to match new JSON keys from Gemini ---
        resultDiv.innerHTML = `
            <h3>Diagnosis Results</h3>
            <p><strong>Plant:</strong> ${data.plant_name || 'N/A'}</p>
            <p><strong>Health Status:</strong> ${data.health_status || 'N/A'}</p>
            <p><strong>Diagnosis:</strong> ${data.diagnosis_details || 'N/A'}</p>
            <p><strong>Suggested Treatment:</strong> ${data.organic_treatment || 'N/A'}</p>
            <p><strong>Watering Advice:</strong> ${data.watering_advice || 'N/A'}</p>
        `;
    }
});
