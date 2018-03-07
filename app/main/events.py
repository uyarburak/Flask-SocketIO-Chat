from flask import session, request
from flask_socketio import emit, join_room, leave_room
from .. import socketio

rooms = {}
@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message and public keys are broadcast to all people in the room."""

    room = session.get('room')

    if room not in rooms:
        rooms[room] =  {}
    person = {'name': session.get('name'), 'publicX': message['pubX'], 'publicY': message['pubY']}
    rooms[room][request.sid] = person
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.', 'keys' : rooms[room]}, room=room)
    dump(message)


@socketio.on('ciphers', namespace='/chat')
def ciphers(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    # emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room, broadcast=True, include_self=False)
    for pair in message['arr']:
        print (pair)
        emit('message', {'sender': request.sid, 'cipher': pair['message']}, room=pair['sid'])
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