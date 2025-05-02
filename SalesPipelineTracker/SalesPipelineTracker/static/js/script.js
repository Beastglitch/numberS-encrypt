document.addEventListener('DOMContentLoaded', function() {
    const inputText = document.getElementById('inputText');
    const encryptBtn = document.getElementById('encryptBtn');
    const decryptBtn = document.getElementById('decryptBtn');
    const clearBtn = document.getElementById('clearBtn');
    const resultArea = document.getElementById('encryptedText');
    const errorArea = document.getElementById('errorMessage');
    const formatSwitch = document.getElementById('formatSwitch');
    const resultLabel = document.getElementById('resultLabel');

    // Function to encrypt text
    function encryptText() {
        const text = inputText.value.trim();
        const useCommas = formatSwitch.checked;
        
        if (!text) {
            showError('Please enter some text to encrypt');
            return;
        }

        // Clear any previous errors
        clearError();
        
        fetch('/encrypt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'text': text,
                'use_commas': useCommas
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server error occurred');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                showError(data.error);
            } else {
                resultLabel.textContent = 'Encrypted Result:';
                resultArea.textContent = data.encrypted;
                resultArea.parentElement.classList.remove('d-none');
            }
        })
        .catch(error => {
            showError(error.message);
        });
    }

    // Function to decrypt text
    function decryptText() {
        const text = inputText.value.trim();
        
        if (!text) {
            showError('Please enter some text to decrypt');
            return;
        }

        // Clear any previous errors
        clearError();
        
        fetch('/decrypt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'text': text
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server error occurred');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                showError(data.error);
            } else {
                resultLabel.textContent = 'Decrypted Result:';
                resultArea.textContent = data.decrypted;
                resultArea.parentElement.classList.remove('d-none');
            }
        })
        .catch(error => {
            showError(error.message);
        });
    }

    // Function to show errors
    function showError(message) {
        errorArea.textContent = message;
        errorArea.classList.remove('d-none');
    }

    // Function to clear errors
    function clearError() {
        errorArea.textContent = '';
        errorArea.classList.add('d-none');
    }

    // Function to clear the form
    function clearForm() {
        inputText.value = '';
        resultArea.textContent = '';
        resultArea.parentElement.classList.add('d-none');
        clearError();
    }

    // Event listeners
    encryptBtn.addEventListener('click', encryptText);
    decryptBtn.addEventListener('click', decryptText);
    clearBtn.addEventListener('click', clearForm);

    // Allow Enter key to submit the form (default to encrypt)
    inputText.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            encryptText();
        }
    });
});
