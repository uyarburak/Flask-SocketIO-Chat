from flask import session, request
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from .kripto import encryptAES, decryptAES, generateRandomString
from .users import getUser, setUsersTokenAndSessionKey
import json

rooms = {}
secrets = {}
@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message and public keys are broadcast to all people in the room."""
    username = message['username']
    ciphertext = message['secret_message']
    user = getUser(username)
    plaintext = json.loads(decryptAES(user['session_key'], ciphertext))
    if(user['sso_token'] != plaintext['sso_token']):
        emit('quit', {}, include_self=True, Broadcast=False)
    room = plaintext['room']
    user_keys = plaintext['payload']
    if room not in rooms:
        rooms[room] =  {}
        secrets[room] =  {}
    rooms[room][request.sid] = {'name': username, 'publicX': user_keys['pubX'], 'publicY': user_keys['pubY']}
    secrets[room][request.sid] = user['session_key']
    for sid in rooms[room]:
        prsn = rooms[room][sid]
        secret = secrets[room][sid]
        print(secret)
        msg = {'msg': username + ' has entered the room.', 'keys' : rooms[room]}
        emit('status', encryptAES(secret, json.dumps(msg)), room=sid)
    dump(message)


@socketio.on('ciphers', namespace='/chat')
def ciphers(message):
    username = message['username']
    ciphertext = message['secret_message']
    user = getUser(username)
    plaintext = json.loads(decryptAES(user['session_key'], ciphertext))
    print('lol ' + json.dumps(plaintext))
    if(user['sso_token'] != plaintext['sso_token']):
        emit('quit', {}, include_self=True, Broadcast=False)
    room = plaintext['room']
    # emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room, broadcast=True, include_self=False)
    for pair in plaintext['payload']:
        print (pair)
        msg = {'sender': request.sid, 'cipher': pair['message'], 'checksum': pair['checksum']}
        secret = secrets[room][pair['sid']]
        emit('message', encryptAES(secret, json.dumps(msg)), room=pair['sid'])
    dump(message)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    del rooms[room][request.sid]
    emit('status', {'msg': session.get('name') + ' has left the room.', 'keys' : rooms[room]}, room=room)
    dump(message)

def dump(message):
    emit('message', {'message' : str(message), 'sender' : session.get('name'), 'room' : session.get('room')}, namespace='/dump', broadcast=True)