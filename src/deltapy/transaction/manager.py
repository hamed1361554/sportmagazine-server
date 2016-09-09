'''
Created on Dec 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import threading
import datetime
import weakref 

from deltapy.core import DeltaObject, DeltaException
from deltapy.utils.uniqueid import get_uuid


class TransactionException(DeltaException):
    pass

class Transaction(DeltaObject):
    '''
    Transaction class.
    '''
    
    class StatusEnum:
        '''
        Transaction status enumeration.
        '''
        
        # ACTIVE is the initial state.
        ACTIVE = "Active"
    
        COMMITTING = "Committing"
        COMMITTED = "Committed"
        
        ROLLING_BACK = "Rolling back"
        ROLLED_BACK = "Rolled back"
    
        # commit() or commit(True) raised an exception.  All further attempts
        # to commit or join this transaction will raise TransactionFailedError.
        COMMIT_FAILED = "Commit failed"
        
        
    def __init__(self, manager, connection, auto_commit = False, parent = None):
        DeltaObject.__init__(self)
        
#        self.__status = Transaction.StatusEnum.ACTIVE
#        self._manager = manager
#        self._childs = []
#        self._parent = parent
#        self.connection = connection
#        self.id = get_uuid()
#        self.creation_date = datetime.datetime.now()         
#        if self._parent:
#            self._parent._childs.append(self)
#        self._auto_commit = auto_commit
#        self._finalized = False

        self.__status = Transaction.StatusEnum.ACTIVE
        self.__manager = weakref.ref(manager)
        self._childs = []
        self.__parent = None
        if parent:
            self.__parent = weakref.ref(parent)
        self.__connection = weakref.ref(connection)
        self.id = get_uuid()
        self.creation_date = datetime.datetime.now()         
        if self.get_parent():
            self.get_parent()._childs.append(self)
        self._auto_commit = auto_commit
        self._finalized = False
        self._after_rollback_triggers = []
        self._before_rollback_triggers = []
        self._before_commit_triggers = []
        self._after_commit_triggers = []
        
    def add_before_commit_trigger(self, trigger, *params):
        '''
        Adds committing triggers.  
        
        @param trigger: this function will be run before committing transaction
        @param *params: trigger parameters
        '''

        if self.__parent is not None:
            return self.__parent.add_before_commit_trigger(trigger, *params)
        if trigger is not None:
            self._before_commit_triggers.append((trigger, params))

    def get_before_commit_triggers(self):
        '''
        Returns added triggers which must be run before committing this transaction.
        @return: []
        '''

        if self.__parent is not None:
            return self.__parent.get_before_commit_triggers()
        return self._before_commit_triggers

            
    def add_after_commit_trigger(self, trigger, *params):
        '''
        Adds committing triggers.  
        
        @param trigger: this function will be run after committing transaction
        @param *params: trigger parameters
        '''

        if self.__parent is not None:
            return self.__parent.add_after_commit_trigger(trigger, *params)
        if trigger is not None:
            self._after_commit_triggers.append((trigger, params))

    def get_after_commit_triggers(self):
        '''
        Returns added triggers which must be run after committing this transaction.
        @return: []
        '''

        if self.__parent is not None:
            return self.__parent.get_after_commit_triggers()
        return self._after_commit_triggers

    def add_before_rollback_trigger(self, trigger, *params):
        '''
        Adds rolling back triggers.  
        
        @param trigger: this function will be run before rolling back transaction
        @param *params: trigger parameters
        '''

        if self.__parent is not None:
            return self.__parent.add_before_rollback_trigger(trigger, *params)
        if trigger is not None:
            self._before_rollback_triggers.append((trigger, params))

    def get_before_rollback_triggers(self):
        '''
        Returns added triggers which must be run before rolling back this transaction.
        @return: []
        '''

        if self.__parent is not None:
            return self.__parent.get_before_rollback_triggers()
        return self._before_rollback_triggers

            
    def add_after_rollback_trigger(self, trigger, *params):
        '''
        Adds rolling back triggers.  
        
        @param trigger: this function will be run after rolling back transaction
        @param *params: trigger parameters
        '''

        if self.__parent is not None:
            return self.__parent.add_after_rollback_trigger(trigger, *params)
        if trigger is not None:
            self._after_rollback_triggers.append((trigger, params))

    def get_after_rollback_triggers(self):
        '''
        Returns added triggers which must be run after rolling back this transaction.
        @return: []
        '''

        if self.__parent is not None:
            return self.__parent.get_after_rollback_triggers()
        return self._after_rollback_triggers

    def __del__(self):
        try:
            self.finalize()
        except:
            pass
        del self._childs
        del self
                
    def finalize(self):
        if not self._finalized:
            if self.get_status() == Transaction.StatusEnum.ACTIVE:
                if self._auto_commit:
                    self.commit()
                else:
                    self.rollback()
        self._finalized = True
        
    def get_manager(self):
        return self.__manager()
    
    def commit(self):        
        if self.is_commitable():
            self._set_status_(Transaction.StatusEnum.COMMITTING)
            if self.get_manager().commit(self):
                self._set_status_(Transaction.StatusEnum.COMMITTED)
        else:
            self._set_status_(Transaction.StatusEnum.COMMIT_FAILED)
            self.get_manager().rollback(self)
    
    def rollback(self):
        self._set_status_(Transaction.StatusEnum.ROLLING_BACK) 
        if self.get_manager().rollback(self):
            self._set_status_(Transaction.StatusEnum.ROLLED_BACK)
            
    def _set_status_(self, status):
        #for child in self._childs:
        #    child._set_status_(status)
        self.__status = status
        
    def is_commitable(self):
        if self.get_status() == Transaction.StatusEnum.COMMITTED:
            raise TransactionException("Transaction[%s] already commited." % str(self)) 
        
        for child in self._childs:
            if child.get_status() == Transaction.StatusEnum.ACTIVE and not child._auto_commit:
                return False            
            if not child.is_commitable():
                return False

        return self.get_status() in (Transaction.StatusEnum.COMMITTING, Transaction.StatusEnum.ACTIVE) 
            
    def get_status(self):
        return self.__status 
    
    def get_parent(self):
        if self.__parent:
            return self.__parent()
        return None
    
    def get_connection(self):
        return self.__connection()
    
    def get_id(self):
        '''
        Returns transaction ID.
        '''
        
        return self.id
    
    def __str__(self):
        return "%s-->%s " % (self.id, self.get_parent())

    def __enter__(self):
        return self
    
    def __exit__(self, type_, value_, traceback_):
        if isinstance(value_, Exception):
            self.rollback()
        else:
            self.commit()
            
    def get_root(self):
        '''
        Returns the root transaction.
        '''
        
        root = self.get_parent()
        if root is None:
            return self
        return root.get_root()

class TwoPhaseCommitTransaction(Transaction):
    
    def __commit_childs__(self):
        for child in self._childs:
            self.get_manager().commit(child)    

    def __rollback_childs__(self):
        for child in self._childs:
            self.get_manager().commit(child)    

    def commit(self):
        if self.is_commitable():
            self._set_status_(Transaction.StatusEnum.COMMITTING)
            if not self.get_parent():                
                self.__commit_childs__()
                self._set_status_(Transaction.StatusEnum.COMMITTED)
        else:
            self._set_status_(Transaction.StatusEnum.COMMIT_FAILED)
            if not self.get_parent():
                self.__rollback_childs__()
    
    def rollback(self):
        self._set_status_(Transaction.StatusEnum.ROLLING_BACK) 
        if not self.get_parent():
            self.__rollback_childs__()
            self._set_status_(Transaction.StatusEnum.ROLLED_BACK)
            
class TransactionManager(DeltaObject):
    
    DEFAULT_TRANSACTION = 'default'
    
    def __init__(self, database_manager):
        DeltaObject.__init__(self)        
        
        self._database_manager = database_manager
        self._transactions = {}

    def get_database_manager(self):
        '''
        Returns database manager.
        
        @return: DatabaseManager 
        '''
        return self._database_manager
    
    def __add_root_transaction__(self, pool_name, trx):
        pool_stack =  self._transactions.get(pool_name, [])
        pool_stack.append(weakref.ref(trx))
        self._transactions[pool_name] = pool_stack
        
    def __remove_root_transaction__(self, pool_name):
        pool_stack =  self._transactions.get(pool_name, [])
        pool_stack.pop()
        
    def __get_current_root_transaction__(self, pool_name):
        pool_stack =  self._transactions.get(pool_name, [])
        if len(pool_stack) > 0:
            return pool_stack[len(pool_stack) - 1]()
        return None
        
    def begin(self, **kargs):
        '''
        Begins a transaction and return it.
        
        @param auto_commit: auto commit flag
        @param pool_name: connection pool name
        @param is_root: root transaction flag 
        
        @return: Transaction
        '''

        auto_commit = kargs.get('auto_commit', False)
        pool_name = kargs.get('pool_name', TransactionManager.DEFAULT_TRANSACTION)
        if not pool_name:
            pool_name = TransactionManager.DEFAULT_TRANSACTION
        
        is_root = kargs.get('is_root', False)

        parent_transaction = None
        connection = None               
        
        if not is_root:
            parent_transaction = self.__get_current_root_transaction__(pool_name)
                              
        if not issubclass(type(parent_transaction), TwoPhaseCommitTransaction):
            if parent_transaction is not None:
                connection = parent_transaction.get_connection()
            else:
                connection = self._database_manager.open(pool_name)
         
        trx = Transaction(self, connection, auto_commit, parent_transaction)
        trx._pool_name = pool_name
        
        if not parent_transaction:
            connection.transaction = trx
            self.__add_root_transaction__(pool_name, trx)
            
        return trx
       
    def _run_before_commit_triggers_(self, tx):
        '''
        '''
        triggers = tx.get_before_commit_triggers()
        if len(triggers) > 0:
            for trigger, params in triggers:
                trigger(*params)
    
    def _run_after_commit_triggers_(self, tx):
        '''
        '''
        triggers = tx.get_after_commit_triggers()
        if len(triggers) > 0:
            for trigger, params in triggers:
                trigger(*params)

    def commit(self, tx):
        try:      
            if not tx.get_parent():
                tx.get_connection().transaction = None
                
                self._run_before_commit_triggers_(tx)
                tx.get_connection().commit()
                self._run_after_commit_triggers_(tx)
                
                self._database_manager.close(tx.get_connection())
                self.__remove_root_transaction__(tx._pool_name)

                return True
        except Exception:
            self.rollback(tx)
            raise
        return False
    
    def _run_before_rollback_triggers_(self, tx):
        '''
        '''
        triggers = tx.get_before_rollback_triggers()
        if len(triggers) > 0:
            for trigger, params in triggers:
                trigger(*params)
    
    def _run_after_rollback_triggers_(self, tx):
        '''
        '''
        triggers = tx.get_after_rollback_triggers()
        if len(triggers) > 0:
            for trigger, params in triggers:
                trigger(*params)

    def rollback(self, tx):
        try:  
            if not tx.get_parent():
                tx.get_connection().transaction = None

                self._run_before_rollback_triggers_(tx)
                tx.get_connection().rollback()
                self._run_after_rollback_triggers_(tx)
                
                self._database_manager.close(tx.get_connection())
                self.__remove_root_transaction__(tx._pool_name)
                return True
        except Exception, e:
            print str(e)
        return False
    
    def tpc_begin(self):
        return TwoPhaseCommitTransaction()      
    
    def get_current_transaction(self, pool_name = None):
        if pool_name is None:
            pool_name = TransactionManager.DEFAULT_TRANSACTION 
        
        parent_transaction = self.__get_current_root_transaction__(pool_name)
        
        return parent_transaction
    
    def cleanup(self):
        for pool_stack in self._transactions.values():
            for trx_proxy in pool_stack:
                if trx_proxy:
                    trx = trx_proxy()
                    if trx:
                        trx.finalize()
        self._transactions.clear()

        
    def __str__(self):
        return "%s" % self._transactions.values()
    
class ThreadTransactionManager(TransactionManager):
    '''
    Provides transaction management on threads.
    '''
    def __init__(self, database_manager):
        TransactionManager.__init__(self, database_manager)
        self.cleanup()
        
#    def __del__(self):
#        pass
        
    def get_transaction_manager(self):
        '''
        Returns local thread or current thread transaction manager.
        
        @return: TransactionManager
        '''
        
        current_thread = threading.currentThread()
        if not hasattr(current_thread, 'transaction_manager'):
            current_thread.transaction_manager = TransactionManager(self._database_manager)        
        return current_thread.transaction_manager
    
    def begin(self, **kargs):
        '''
        Begins a transaction and return it.
        
        @param auto_commit: auto commit flag
        @param pool_name: connection pool name
        
        @return: Transaction
        '''
        
        return self.get_transaction_manager().begin(**kargs)
        
    def commit(self, trx):
        return self.get_transaction_manager().commit(trx) 
    
    def rollback(self, trx):
        return self.get_transaction_manager().rollback(trx)
        
    def tpc_begin(self):
        return self.get_transaction_manager().tpc_begin()  
    
    def get_current_transaction(self, pool_name = None):
        return self.get_transaction_manager().get_current_transaction(pool_name)
    
    def cleanup(self):
        current_thread = threading.currentThread()
        if hasattr(current_thread, 'transaction_manager'):
            transaction_manager = getattr(current_thread, 'transaction_manager') 
            transaction_manager.cleanup()
            delattr(current_thread, 'transaction_manager')
            del transaction_manager