from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json  # Get JSON data from the POST request
    # Process the received data as needed
    print("Received data:", data)
    # Optionally, you can send a response back to the Chrome extension
    response_data = {"status": "success"}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
