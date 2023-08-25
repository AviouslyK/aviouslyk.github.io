from flask import Flask, request, jsonify
from flask_cors import CORS
from word_correlator import WordCorrelator  # Import existing WordCorrelator class

app = Flask(__name__)
CORS(app) # allow requests from github website domain to access resources from this server
correlator = WordCorrelator()  # Initialize the WordCorrelator instance

@app.route('/process_guess', methods=['POST'])
def process_guess():
    data = request.get_json()  # Get the JSON data from the request
    guess = data.get('guess')  # Extract the user's guess

    # Calculate similarity score using WordCorrelator class
    similarity_score = correlator.calculate_similarity_score(guess)

    # Prepare the response data
    response_data = {
        'score': similarity_score
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 

