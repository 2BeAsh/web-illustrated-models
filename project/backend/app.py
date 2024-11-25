from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/model", methods=["POST"])
def model():
    data = request.json
    # Example: Simulate running a model
    params = data.get("parameters", {})  # Second argument is default value
    result = {key: value ** 2 for key, value in params.items()}  # Dummy calculation
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)