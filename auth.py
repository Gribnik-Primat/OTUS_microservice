from flask import Flask, request, jsonify
import jwt
import uuid

app = Flask(__name__)

SECRET_KEY = 'your-secret-key'

tank_battles = {}

@app.route('/create_battle', methods=['POST'])
def create_battle():
    data = request.get_json()
    participants = data.get('participants', [])
    battle_id = str(uuid.uuid4())
    tank_battles[battle_id] = participants
    return jsonify({'battle_id': battle_id})

@app.route('/get_token', methods=['POST'])
def get_token():
    data = request.get_json()
    user_id = data.get('user_id')
    battle_id = data.get('battle_id')
    if user_id in tank_battles.get(battle_id, []):
        token = jwt.encode({'user_id': user_id, 'battle_id': battle_id}, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'User is not a participant of this battle'}), 403


if __name__ == '__main__':
    app.run()
