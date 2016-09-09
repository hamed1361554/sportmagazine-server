'''
Created on Aug 19, 2009

@author: mohammadi, vesal
'''

from deltapy.locals import *

def run_script_module(script_module,run_name = None):
    return get_app_context()[APP_SCRIPTING].run_script_module(script_module,run_name)
    
def execute_script(script):
    get_app_context()[APP_SCRIPTING].execute_script(script)

def evaluate_expr(expr):
    return get_app_context()[APP_SCRIPTING].evaluate_expr(expr)
