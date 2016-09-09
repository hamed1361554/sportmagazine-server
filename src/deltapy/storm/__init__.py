
from deltapy.packaging.package import Package
from deltapy.locals import *
from storm.variables import RawStrVariable
from storm.properties import SimpleProperty
import storm.database

class BufferVariable(RawStrVariable):
    __slots__ = ()
    def parse_set(self, value, from_db):
        if isinstance(value, str):
            value = buffer(value)
        return value
    
    def parse_get(self, value, to_db):
        if not to_db:
            return str(value)
        if to_db:
            if isinstance(value, str):
                value = buffer(value)
            return value
        return str(value)

class Buffer(SimpleProperty):
    variable_class = BufferVariable
                    
def get_many(self, count):
    """Fetch all results from the cursor.

    The results will be converted to an appropriate format via
    L{from_database}.

    @raise DisconnectionError: Raised when the connection is lost.
        Reconnection happens automatically on rollback.
    """
    result = self._connection._check_disconnect(self._raw_cursor.fetchmany, count)
    if result:
       return [tuple(self.from_database(row)) for row in result]
    return result

class StormPackage(Package):
    def load(self):
        storm.database.Result.get_many = get_many
     
    def unload(self):
        pass
    
