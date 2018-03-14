# These events must do the challenge-response authentication

from flask import session, request
from flask_socketio import emit
from .. import socketio
from .users import getUser, setUsersTokenAndSessionKey
from .kripto import decryptRSA, encryptAES, decryptAES, generateRandomString
from hashlib import sha256
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

@socketio.on('start_protocol', namespace='/auth')
def start_protocol(message):
    user = getUser(message['name'])
    random_challenge = generateRandomString()
    user['challenge'] = random_challenge
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

    if user['challenge'] != obj['challenge']:
        error_message('You sent the wrong challenge')
    else:
        # User sent the right challenge
        # Server should give client a sso_token with session_key encrypted
        sso_token = generateRandomString(20)
        setUsersTokenAndSessionKey(message['name'], sso_token, obj['session_key'])
        encryptedToken = encryptAES(obj['session_key'], sso_token)
        emit('protocol_level_2', {'sso_token': encryptedToken}, include_self=True, Broadcast=False)
        error_message('You sent the right challenge')
        dump('Server sents sso_token: ' + sso_token + '\nEncrypted version: ' + encryptedToken, user['name'])


def dump(message, sender):
    emit('message', {'message' : str(message) + "\n", 'sender' : sender, 'room' : ""}, namespace='/dump', broadcast=True)

def error_message(message):
    emit('error_message', {'message' : str(message)}, include_self=True, Broadcast=False)