'''
Created on Jan 21, 2012

@author: Abi M.Sangarab, Majid Vesal
'''

import pyDes
import string
import random
from Crypto.Cipher import AES

def encrypt(text):
    '''
    Returns encrypted key.

    @param text: text
    '''

    key = '0906630f-7346-4697-8fd0-'
    des = pyDes.triple_des(key)
    return des.encrypt(text, padmode = pyDes.PAD_PKCS5)

def decrypt(crypted_text):
    '''
    Returns encrypted key.

    @param text: text
    '''

    key = '0906630f-7346-4697-8fd0-'
    des = pyDes.triple_des(key)
    return des.decrypt(crypted_text, padmode = pyDes.PAD_PKCS5)

def encrypt_aes(text):
    '''
    Returns encrypted key in aes algorithm
    @param str text: text
    @rtype str
    '''
    pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

    message = pad(text)
    key = '\x87\xd7\xdc;\xb4,S_\xb7\xae\x0b\xbf\xb7\xa6\x8d6\x88_\xd8=\x8bV\xdb\xed\x080\x95\x8am\x86\x1e\xa3'
    # Generate a 16 char string randomly
    random_IV = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])

    obj = AES.new(key, AES.MODE_CBC, random_IV)
    # Concate IV to the end of encrypt message
    # to use in decryption the same IV
    z = obj.encrypt(message) + random_IV
    return z

def decrypt_aes(text):
    '''
    Returns decrypted key in aes algorithm
    @param str text: text
    @rtype str
    '''

    unpad = lambda s : s[0:-ord(s[-1])]
    key = '\x87\xd7\xdc;\xb4,S_\xb7\xae\x0b\xbf\xb7\xa6\x8d6\x88_\xd8=\x8bV\xdb\xed\x080\x95\x8am\x86\x1e\xa3'
    IV = text[len(text)-16:len(text)]
    obj = AES.new(key, AES.MODE_CBC, IV)
    # Last 16 char is IV and first part is
    # text to decrypt.
    x = obj.decrypt(text[0:len(text)-16])
    return unpad(x)
