# These events must do the challenge-response authentication

from flask import session, request
from flask_socketio import emit
from .. import socketio
from .users import getUser
from .kripto import decryptRSA, encryptAES, decryptAES
from hashlib import sha256
import string
import random
import hmac
import json

def hmac_sha256(secret_key, string):
    string_to_sign = string.encode('utf-8')
    key_to_sign = secret_key.encode('utf-8')
    hashed = hmac.new(key_to_sign,string_to_sign, sha256)
    return hashed.hexdigest()

def hex_sha1(string):
    string_to_sign = string.encode('utf-8')
    hashed = sha256(string_to_sign)
    return hashed.hexdigest()

def generateRandomChallenge(length=15):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

@socketio.on('start_protocol', namespace='/auth')
def start_protocol(message):
    user = getUser(message['name'])
    random_challenge = generateRandomChallenge()
    print ("random challenge: ", random_challenge)
    ciphertext = encryptAES(user['password'], random_challenge)
    print ("ciphertext: ", ciphertext)
    emit('protocol_level_1', {'challenge': ciphertext}, include_self=True, Broadcast=False)
    dump('Server creates a random challenge: ' + random_challenge + '\nAES256 encrypts with the user\'s hashed_password: ' + user['password'] + "\nCiphertext: " + ciphertext, user['name'])

@socketio.on('proof_of_id', namespace='/auth')
def proof_of_id(message):
    user = getUser(message['name'])
    ciphertext = message['ciphertext']
    plaintext = decryptRSA(ciphertext)
    obj = json.loads(plaintext)
    print ("given challenge: ", obj['challenge'])
    print ("given session_key: ", obj['session_key'])
    dump('User sent a RSA encrypted message: ' + ciphertext + '\nServer decrypts it... Payload is: {challenge: \'\n' + obj['challenge'] + "\', session_key: \'" + obj['session_key'] +"\'}", user['name'])


def dump(message, sender):
    emit('message', {'message' : str(message) + "\n", 'sender' : sender, 'room' : ""}, namespace='/dump', broadcast=True)