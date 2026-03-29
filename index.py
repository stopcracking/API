from flask import Flask, jsonify, request
import time

app = Flask(__name__)

# The Master State
state = {
    "command": "none", 
    "message": "",
    "target_player": "",
    "target_alt": "all",
    "alts": {} # Stores { "Username": {"thumb": "url", "status": "Online", "last_seen": 12345} }
}

@app.route('/poll', methods=['GET'])
def poll():
    return jsonify(state)

@app.route('/register', methods=['POST'])
def register():
    global state
    data = request.get_json()
    username = data.get("username")
    if username:
        state["alts"][username] = {
            "thumb": data.get("thumb"),
            "status": "Online",
            "last_seen": time.time()
        }
    return jsonify({"success": True})

@app.route('/update', methods=['POST'])
def update():
    global state
    state.update(request.get_json())
    return jsonify(state), 200

def handler(request):
    return app(request)
