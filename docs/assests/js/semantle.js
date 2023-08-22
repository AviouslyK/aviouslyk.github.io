const guessInput = document.getElementById("guessInput");
const guessButton = document.getElementById("guessButton");
const outputArea = document.getElementById("outputArea");

guessButton.addEventListener("click", () => {
    const guess = guessInput.value;
    
    // Send the guess to the server using AJAX or fetch
    // Replace 'SERVER_URL' with the actual URL of your server
    const SERVER_URL = 'http://localhost:5000';  // Change port if needed

guessButton.addEventListener("click", () => {
    const guess = guessInput.value;

    fetch(`${SERVER_URL}/process_guess`, {
        method: 'POST',
        body: JSON.stringify({ guess }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        outputArea.textContent = `Similarity Score: ${data.score}`;
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });    
});
});
