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

    person = {'publicX': message['pubX'], 'publicY': message['pubY']}
    rooms[room][session.get('name')] = person
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.', 'keys' : rooms[room]}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room, broadcast=True, include_self=False)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

