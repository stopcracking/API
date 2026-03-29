from flask import Flask, jsonify, request
import time

app = Flask(__name__)

# This prevents the 404 on the main page
@app.route('/')
def home():
    return "<h1>Bridge is Online</h1><p>Vercel is correctly running index.py from the root.</p>"

state = {
    "command": "none", 
    "message": "",
    "target_player": "",
    "target_alt": "all",
    "alts": {} 
}

@app.route('/poll', methods=['GET'])
def poll():
    return jsonify(state)

# ... (keep your /register and /update routes here) ...

# REQUIRED FOR VERCEL
if __name__ == "__main__":
    app.run()
