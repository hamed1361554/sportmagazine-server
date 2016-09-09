'''
Created on Jan 21, 2012

@author: Abi M.Sangarab, Majid Vesal
'''

import pyDes

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

    