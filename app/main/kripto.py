# Imports to use RSA
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto import Random
# Imports to use AES
import pyaes
import binascii
import random
import string

decryptorRSA = None;
sentinel = None;

def initKripto():
    global decryptorRSA, sentinel
    # Initalize the RSA keys
    e = long('10001', 16)
    n = long('a5261939975948bb7a58dffe5ff54e65f0498f9175f5a09288810b8975871e99af3b5dd94057b0fc07535f5f97444504fa35169d461d0d30cf0192e307727c065168c788771c561a9400fb49175e9e6aa4e23fe11af69e9412dd23b0cb6684c4c2429bce139e848ab26d0829073351f4acd36074eafd036a5eb83359d2a698d3', 16)
    d = long('8e9912f6d3645894e8d38cb58c0db81ff516cf4c7e5a14c7f1eddb1459d2cded4d8d293fc97aee6aefb861859c8b6a3d1dfe710463e1f9ddc72048c09751971c4a580aa51eb523357a3cc48d31cfad1d4a165066ed92d4748fb6571211da5cb14bc11b6e2df7c1a559e6d5ac1cd5c94703a22891464fba23d0d965086277a161', 16)
    p = long('d090ce58a92c75233a6486cb0a9209bf3583b64f540c76f5294bb97d285eed33aec220bde14b2417951178ac152ceab6da7090905b478195498b352048f15e7d', 16)
    key = RSA.construct((n, e, d, p))
    # Initiliaze the RSA decryptor
    sentinel = Random.new().read(15+SHA.digest_size)      # Let's assume that average data length is 15
    decryptorRSA = PKCS1_v1_5.new(key)

def decryptRSA(ciphertext):
    ciphertextLong = "".join([chr(int(ciphertext[x:x+2], 16)) for x in range(0, len(ciphertext), 2)])
    decrypted = decryptorRSA.decrypt(ciphertextLong, sentinel).decode('utf-8')
    return decrypted

def encryptAES(key, plaintext):
    counter = pyaes.Counter(initial_value = 5)
    aes = pyaes.AESModeOfOperationCTR(bytearray.fromhex(key), counter = counter)
    ciphertext = aes.encrypt(plaintext)
    return binascii.hexlify(ciphertext)

def decryptAES(key, ciphertext):
    counter = pyaes.Counter(initial_value = 5)
    aes = pyaes.AESModeOfOperationCTR(bytearray.fromhex(key), counter = counter)
    strCipherText = "".join([chr(int(ciphertext[x:x+2], 16)) for x in range(0, len(ciphertext), 2)])
    return aes.decrypt(strCipherText)

def generateRandomString(length=10):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))