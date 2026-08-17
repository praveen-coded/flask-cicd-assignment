from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello from Flask CI/CD Pipeline!"


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/error")
def error():
    return jsonify({
        "status": "error"
    }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
    
