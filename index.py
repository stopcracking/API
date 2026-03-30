from flask import Flask, jsonify, request
import time

app = Flask(__name__)

# Global Hub State
state = {
    "command": "none",
    "message": "",
    "selected_alts": ["all"], # Stores list of alts to control
    "alts": {} # Stores: {"Username": {"thumb": "url", "last_seen": 12345}}
}

@app.route('/')
def home():
    return f"Bridge Online. Connected Alts: {len(state['alts'])}"

@app.route('/poll', methods=['GET'])
def poll():
    # Cleanup: Remove alts that haven't checked in for 10 minutes
    current_time = time.time()
    state["alts"] = {
        name: info for name, info in state["alts"].items() 
        if current_time - info["last_seen"] < 600
    }
    return jsonify(state)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True, silent=True)
    if data and "username" in data:
        username = data["username"]
        state["alts"][username] = {
            "thumb": data.get("thumb", ""),
            "last_seen": time.time()
        }
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Missing username"}), 400

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json(force=True, silent=True)
    if data:
        # Updates command, message, or selected_alts list
        state.update(data)
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 400

if __name__ == "__main__":
    app.run()
