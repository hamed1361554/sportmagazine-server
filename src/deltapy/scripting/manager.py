'''
Created on Aug 19, 2009

@author: mohammadi, vesal
'''

import runpy
from deltapy.core import DeltaObject, DeltaException

class ScriptManager(DeltaObject):
    
    def __init__(self):
        DeltaObject.__init__(self)
    
    def run_script_module(self, script_module,run_name = None):
        return runpy.run_module(script_module, init_globals = None, run_name = None, alter_sys = False)
        
    def execute_script(self, script):
        exec script
    
    def evaluate_expr(self, expr):
        return eval(expr)
