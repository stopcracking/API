from flask import Flask, jsonify, request

app = Flask(__name__)

# Global state to store your spam info
state = {"message": "Waiting...", "enabled": False}

@app.route('/')
def home():
    return "Bridge is Online."

@app.route('/poll', methods=['GET'])
def poll():
    return jsonify(state)

@app.route('/update', methods=['POST'])
def update():
    global state
    data = request.get_json()
    if data:
        state["message"] = data.get("message", state["message"])
        state["enabled"] = data.get("enabled", state["enabled"])
    return jsonify({"status": "success", "current": state}), 200

# Vercel requirements
def handler(request):
    return app(request)