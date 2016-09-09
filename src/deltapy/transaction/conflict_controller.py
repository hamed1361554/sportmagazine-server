'''
Created on May 8, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from threading import Event

from deltapy.utils.concurrent import ConflictController
from deltapy.transaction.services import get_current_transaction

class TransactionalConflictController(ConflictController):
    '''
    Controls conflict of lists items.
    '''
    
    def __init__(self):
        ConflictController.__init__(self)

    def _add_to_queue_(self, lst):
        try:
            self._lock.acquire()
            
            obj_set, obj_event = self._get_conflicted_list_(lst)
            if obj_event:
                return obj_event

            event = Event()
            event.clear()
            obj_set = set(lst)
            event.transaction_id = self._get_root_transaction_id_()
            self._active_lists[id(lst)] = obj_set, event
            
            return None
        finally:
            self._lock.release()
            
    def _get_root_transaction_id_(self):
        trx = get_current_transaction()
        parent_trx = trx.get_parent()
        if parent_trx is not None:
            return parent_trx.get_id()
        return trx.get_id()

    def _get_conflicted_list_(self, lst):
        transaction_id = self._get_root_transaction_id_()
        current_set = set(lst)
        for obj_set, event in self._active_lists.values():
            if len(current_set.intersection(obj_set)) > 0:
                if event.transaction_id != transaction_id: 
                    return obj_set, event
        return None, None
        