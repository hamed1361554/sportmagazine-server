"""
Created on Sep 9, 2016

@author: Hamed Zekri
"""

import storm.tracer
from server import SportMagazineServerApplication

def f(s):
    return s

__builtins__._ = f

storm.tracer.debug(True)
SportMagazineServerApplication().run()