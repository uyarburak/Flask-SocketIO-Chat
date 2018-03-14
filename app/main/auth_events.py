# These events must do the challenge-response authentication

from flask import session, request
from flask_socketio import emit
from .. import socketio
from .users import getUser
from .kripto import decryptRSA, encryptAES, decryptAES
from hashlib import sha1
import string
import random
import hmac

def hmac_sha1(secret_key, string):
    string_to_sign = string.encode('utf-8')
    key_to_sign = secret_key.encode('utf-8')
    hashed = hmac.new(key_to_sign,string_to_sign, sha1)
    return hashed.hexdigest()

def hex_sha1(string):
    string_to_sign = string.encode('utf-8')
    hashed = sha1(string_to_sign)
    return hashed.hexdigest()

def generateRandomChallenge(length=120):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

@socketio.on('start_protocol', namespace='/auth')
def start_protocol(message):
    user = getUser(message['name'])
    random_challenge = generateRandomChallenge()
    print ("random challenge: ", random_challenge)
    ciphertext = encryptAES(user['password'], random_challenge)
    print ("ciphertext: ", ciphertext)
    emit('protocol_level_1', {'challenge': ciphertext}, include_self=True, Broadcast=False)