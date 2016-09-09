'''
Created on Feb 25, 2010

@author: mohammadi
'''


import os, sys, time

try:
    import thread
except ImportError:
    import dummy_thread as thread

# This import does nothing, but it's necessary to avoid some race conditions
# in the threading module. See http://code.djangoproject.com/ticket/2330 .
try:
    import threading
except ImportError:
    pass


RUN_RELOADER = True

_mtimes = {}
_win = (sys.platform == "win32")

def code_changed():
    global _mtimes, _win
    for filename in filter(lambda v: v, map(lambda m: getattr(m, "__file__", None), sys.modules.values())):
        if filename.endswith(".pyc") or filename.endswith(".pyo"):
            filename = filename[:-1]
        if not os.path.exists(filename):
            continue # File might be in an egg, so it can't be reloaded.
        stat = os.stat(filename)
        mtime = stat.st_mtime
        if _win:
            mtime -= stat.st_ctime
        if filename not in _mtimes:
            _mtimes[filename] = mtime
            continue
        if mtime != _mtimes[filename]:
            _mtimes = {}
            return True
    return False

def reloader_thread():
    while RUN_RELOADER:
        if code_changed():
            sys.exit(3) # force reload
        time.sleep(1)


def start():
    reloader = reloader_thread
    thread.start_new_thread(reloader, args = (), kwargs = None)    

