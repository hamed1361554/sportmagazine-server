'''
Created on Sep 1, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import os
import time

class DirectoryWatcher:
    def __init__(self):
        self._paths = {}
        self._befores = {}
    
    def add_to_watch(self, path, watch_func):              
        watch_funcs = self._paths.get(path, [])
        if not watch_func in watch_funcs:
            watch_funcs.append(watch_func)
        self._paths[path] =  watch_funcs               
    
    def remove_from_watch(self, path):              
        del self._paths[path]               
        del self._befores[path]

    def watch(self):
        """
        this function watches all paths that registered for watching.
        """
        for path_to_watch in self._paths.keys():
            if os.path.exists(path_to_watch):                
                watch_funcs = self._paths[path_to_watch]                                
                after = dict ([(f,None) for f in os.listdir (path_to_watch)])
                before = self._befores.get(path_to_watch, after)
                changed = []
                added = []
                removed = [f for f in before if not f in after]
                #checking for added files and changed file
                for file_name in after.keys():

                    f = os.path.join(path_to_watch,file_name)
                    #setting modification date just for files
                    if os.path.isfile(f):
                        after[file_name] = os.path.getmtime(f)
                       
                    #setting modification date just for files
                    if not file_name in before:
                        added.append(file_name)
                    elif before[file_name] != after[file_name]:
                        changed.append(file_name)
                       
                if (len(added)+len(removed)+len(changed)) > 0:
                    for watch_func in watch_funcs:
                        watch_func(path_to_watch, added, removed, changed)
                
                self._befores[path_to_watch] = after

