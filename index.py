from flask import Flask, jsonify, request
import time

app = Flask(__name__)

# Global Hub State
state = {
    "command": "none",
    "message": "",
    "target_player": "",
    "target_alt": "all",
    "config": {"speed": 16, "jump": 50},
    "alts": {} # Stores: {"Username": {"thumb": "url", "status": "Online", "last_seen": 12345}}
}

@app.route('/')
def home():
    return f"<h1>Bridge is Online</h1><p>Connected Alts: {len(state['alts'])}</p>"

@app.route('/poll', methods=['GET'])
def poll():
    # Optional: Clean up alts that haven't checked in for 10 minutes
    current_time = time.time()
    expired = [name for name, info in state["alts"].items() if current_time - info["last_seen"] > 600]
    for name in expired:
        del state["alts"][name]
        
    return jsonify(state)

@app.route('/register', methods=['POST'])
def register():
    global state
    # force=True ensures it reads the JSON even if the Roblox header is messy
    data = request.get_json(force=True, silent=True)
    
    if data and "username" in data:
        username = data["username"]
        state["alts"][username] = {
            "thumb": data.get("thumb", "https://www.roblox.com/headshot-thumbnail/image?userId=1&width=420&height=420&format=png"),
            "status": "Online",
            "last_seen": time.time()
        }
        return jsonify({"status": "success", "message": f"Registered {username}"}), 200
    
    return jsonify({"status": "error", "message": "Missing username"}), 400

@app.route('/update', methods=['POST'])
def update():
    global state
    data = request.get_json(force=True, silent=True)
    if data:
        # Deep merge for config if it exists
        if "config" in data and isinstance(data["config"], dict):
            state["config"].update(data["config"])
            del data["config"]
            
        state.update(data)
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 400

# Required for Vercel
if __name__ == "__main__":
    app.run()
