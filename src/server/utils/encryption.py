"""
Created on Sep 9, 2016

@author: Hamed Zekri
"""

import random
import string
import base64
from Crypto.Cipher import AES

from hashlib import sha512

secret_key = 'uejfmaohemlepfkq'

def generate_randoms(length=16):
    '''
    Generates random string of given length.

    :param int length: random string length
    :return: random string
    '''

    return ''.join(random.SystemRandom().choice('abcdef' + string.digits) for i in range(length))


def encrypt_sha512(plain, salt=None):
    '''
    Encrypts given plain text with sha512.

    :param str plain: plain message
    :return: encrypted string
    '''

    if salt is None:
        salt = generate_randoms()
    return sha512(salt + plain).hexdigest() + salt


def verify_sha512(plain, cipher):
    '''
    Verifies given cypher text with sha512

    :param plain: plain message
    :param cipher: cipher message
    :return: verification result boolean
    '''

    salt = cipher[-16:]
    return cipher == encrypt_sha512(plain, salt=salt)


def encrypt_aes(plain):
    '''
    Encrypts given plain text with aes.

    :param plain: plain message
    :return: encrypted string
    '''

    msg_text = plain.rjust(((len(plain)/16) + 1)*16)
    msg_iv = generate_randoms()
    cipher = AES.new(secret_key, AES.MODE_CBC, msg_iv)
    return base64.b64encode(cipher.encrypt(msg_text) + msg_iv)


def decrypt_aes(cipher):
    '''
    Decrypts given plain text with aes.

    :param cipher: cipher message
    :return: plain message
    '''

    cipher_text = base64.b64decode(cipher)
    cipher = AES.new(secret_key, AES.MODE_CBC, cipher_text[-16:])
    decoded = cipher.decrypt(cipher_text[:len(cipher_text)-16])
    return decoded.strip()
