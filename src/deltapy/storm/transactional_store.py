'''
Created on Aug 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from storm.locals import Store

try:
    import cx_Oracle
    import decimal

    def NumbersAsDecimal(cursor, name, defaultType, size, precision,
            scale): 
        if defaultType == cx_Oracle.NUMBER: 
            return cursor.var(str, 40, 
                              cursor.arraysize, 
                              outconverter = decimal.Decimal)
         
except ImportError:
    pass

class TransactionalStore(Store):
    def __init__(self, database):
        Store.__init__(self, database)
        #if database.__class__.__name__ == 'Oracle':
        #    self._connection._raw_connection.outputtypehandler = NumbersAsDecimal
        self.transaction = None
        
    def commit(self):
        if self.transaction:
            self.transaction = None
            return self.transaction.commit()      
        result = Store.commit(self)
        #Store.reset(self)
        return result
    
    def rollback(self):
        if self.transaction:
            self.transaction = None
            return self.rollback.commit()
        result = Store.rollback(self)  
        #Store.reset(self)
        return result      
        
