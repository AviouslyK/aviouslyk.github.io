from flask import Flask, request, jsonify
from flask_cors import CORS
from word_correlator import WordCorrelator  # Import existing WordCorrelator class
from game import main  # Import the main function from game.py

app = Flask(__name__)
CORS(app, origins="https://aviouslyk.github.io")# allow requests from github website domain to access resources from this server
correlator = WordCorrelator()  # Initialize the WordCorrelator instance

@app.route('/')
def index():
    return "Welcome to the Word Guessing App!"

@app.route('/start_game', methods=['POST'])
def start_game():
    print("Starting the game...")    
    main() # Call the main function from game.py

    return jsonify({'message': 'Game started successfully'})

@app.route('/process_guess', methods=['POST'])
def process_guess():
    data = request.get_json()  # Get the JSON data from the request
    guess = data.get('guess')  # Extract the user's guess
    app.logger.info(f"Received guess: {guess}")
    
    # Calculate similarity score using WordCorrelator class
    similarity_score = correlator.calculate_similarity_score(guess)

    # Prepare the response data
    response_data = {
        'score': similarity_score
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 

