const guessInput = document.getElementById("guessInput");
const guessButton = document.getElementById("guessButton");
const outputArea = document.getElementById("outputArea");

guessButton.addEventListener("click", () => {
    const guess = guessInput.value;
    
    // Send the guess to the server using fetch
    const SERVER_URL = 'https://52.14.133.15:5000';  // AWS EC2 instance I've set up

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
