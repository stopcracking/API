from flask import Flask, jsonify, request

app = Flask(__name__)

# The Master State
state = {
    "command": "none", 
    "message": "",
    "target_player": "", # Who the alts are attacking
    "target_alt": "all",  # Which alt should listen ("all" or "Username")
    "config": {"speed": 16, "jump": 50},
}

@app.route('/poll', methods=['GET'])
def poll():
    return jsonify(state)

@app.route('/update', methods=['POST'])
def update():
    global state
    state.update(request.get_json())
    return jsonify(state), 200

def handler(request):
    return app(request)
