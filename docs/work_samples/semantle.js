const guessInput = document.getElementById("guessInput");
const guessButton = document.getElementById("guessButton");
const outputArea = document.getElementById("outputArea");

console.log("JavaScript is running!");

// Start the game - load the word correlator model
window.onload = function () {
    // Make an initial request to start the game when the page loads
    const SERVER_URL = 'https://18.118.103.211:5000';

    fetch(`${SERVER_URL}/start_game`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        console.log('Game started successfully!');
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
};


guessButton.addEventListener("click", () => {
    const guess = guessInput.value;
    console.log("Guess:", guess);
    
    // Send the guess to the server using fetch
    const SERVER_URL = 'https://18.118.103.211:5000';  // AWS EC2 instance I've set up

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