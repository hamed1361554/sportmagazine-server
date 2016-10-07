"""
Created on Sep 9, 2016

@author: Hamed Zekri
"""

import random
import string

from hashlib import sha512


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