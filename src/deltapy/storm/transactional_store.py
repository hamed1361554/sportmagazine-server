'''
Created on Aug 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from storm import Undef
from storm.locals import Store
from storm.store import FindSpec, get_where_for_args, ResultSet
from storm.variables import Variable
from storm.info import get_cls_info
from storm.expr import compare_columns, Select
from storm.exceptions import FeatureError

from deltapy.core import DeltaException

try:
    import cx_Oracle
    import decimal

    def NumbersAsDecimal(cursor, name, defaultType, size, precision,
            scale): 
        if defaultType == cx_Oracle.NUMBER: 
            return cursor.var(str, 40, 
                              cursor.arraysize, 
                              outconverter=decimal.Decimal)
         
except ImportError:
    pass


RESOURCE_BUSY_ERROR_CODE = 54
RESOURCE_BUSY_ERROR_MESSAGE = "Resource busy error. Please try again after a few moments."


class DatabaseResourceBusyException(DeltaException):
    """

    """


class DeltaResultSet(ResultSet):

    def __init__(self, store, find_spec,
                 where=Undef, tables=Undef, select=Undef, for_update_nowait=False):
        super(DeltaResultSet, self).__init__(store, find_spec, where, tables, select, for_update_nowait)

    def __iter__(self):
        """
        Iterate the results of the query.
        """
        try:
            result = self._store._connection.execute(self._get_select())
            for values in result:
                yield self._load_objects(result, values)
        except Exception as db_error:
            if db_error[0].code == RESOURCE_BUSY_ERROR_CODE:  # Resource busy
                raise DatabaseResourceBusyException(_(RESOURCE_BUSY_ERROR_MESSAGE))

            raise db_error

    def __contains__(self, item):
        """Check if an item is contained within the result set."""
        try:
            return super(DeltaResultSet, self).__contains__(item)
        except Exception as db_error:
            if db_error[0].code == RESOURCE_BUSY_ERROR_CODE:  # Resource busy
                raise DatabaseResourceBusyException(_(RESOURCE_BUSY_ERROR_MESSAGE))

            raise db_error

    def is_empty(self):
        """Return C{True} if this result set doesn't contain any results."""
        try:
            return super(DeltaResultSet, self).is_empty()
        except Exception as db_error:
            if db_error[0].code == RESOURCE_BUSY_ERROR_CODE:  # Resource busy
                raise DatabaseResourceBusyException(_(RESOURCE_BUSY_ERROR_MESSAGE))

            raise db_error

    def any(self):
        """Return a single item from the result set.

        @return: An arbitrary object or C{None} if one isn't available.
        @seealso: one(), first(), and last().
        """
        try:
            return super(DeltaResultSet, self).any()
        except Exception as db_error:
            if db_error[0].code == RESOURCE_BUSY_ERROR_CODE:  # Resource busy
                raise DatabaseResourceBusyException(_(RESOURCE_BUSY_ERROR_MESSAGE))

            raise db_error

    def _any(self):
        """Return a single item from the result without changing sort order.

        @return: An arbitrary object or C{None} if one isn't available.
        """
        try:
            return super(DeltaResultSet, self)._any()
        except Exception as db_error:
            if db_error[0].code == RESOURCE_BUSY_ERROR_CODE:  # Resource busy
                raise DatabaseResourceBusyException(_(RESOURCE_BUSY_ERROR_MESSAGE))

            raise db_error

    def last(self):
        """Return the last item from an ordered result set.

        @raises FeatureError: Raised if the result set has a C{LIMIT} set.
        @raises UnorderedError: Raised if the result set isn't ordered.
        @return: The last object or C{None} if one isn't available.
        @seealso: first(), one(), and any().
        """
        try:
            return super(DeltaResultSet, self).last()
        except Exception as db_error:
            if db_error[0].code == RESOURCE_BUSY_ERROR_CODE:  # Resource busy
                raise DatabaseResourceBusyException(_(RESOURCE_BUSY_ERROR_MESSAGE))

            raise db_error

    def one(self):
        """Return one item from a result set containing at most one item.

        @raises NotOneError: Raised if the result set contains more than one
            item.
        @return: The object or C{None} if one isn't available.
        @seealso: first(), one(), and any().
        """
        try:
            return super(DeltaResultSet, self).one()
        except Exception as db_error:
            if db_error[0].code == RESOURCE_BUSY_ERROR_CODE:  # Resource busy
                raise DatabaseResourceBusyException(_(RESOURCE_BUSY_ERROR_MESSAGE))

            raise db_error

    def remove(self):
        """Remove all rows represented by this ResultSet from the database.

        This is done efficiently with a DELETE statement, so objects
        are not actually loaded into Python.
        """
        try:
            return super(DeltaResultSet, self).remove()
        except Exception as db_error:
            if db_error[0].code == RESOURCE_BUSY_ERROR_CODE:  # Resource busy
                raise DatabaseResourceBusyException(_(RESOURCE_BUSY_ERROR_MESSAGE))

            raise db_error

    def _aggregate(self, aggregate_func, expr, column=None):
        try:
            return super(DeltaResultSet, self)._aggregate(aggregate_func, expr, column)
        except Exception as db_error:
            if db_error[0].code == RESOURCE_BUSY_ERROR_CODE:  # Resource busy
                raise DatabaseResourceBusyException(_(RESOURCE_BUSY_ERROR_MESSAGE))

            raise db_error

    def values(self, *columns):
        """Retrieve only the specified columns.

        This does not load full objects from the database into Python.

        @param columns: One or more L{storm.expr.Column} objects whose
            values will be fetched.
        @raises FeatureError: Raised if no columns are specified or if this
            result is a set expression such as a union.
        @return: An iterator of tuples of the values for each column
            from each matching row in the database.
        """
        try:
            if not columns:
                raise FeatureError("values() takes at least one column "
                                   "as argument")
            if self._select is not Undef:
                raise FeatureError("values() can't be used with set expressions")
            select = self._get_select()
            select.columns = columns
            result = self._store._connection.execute(select)
            if len(columns) == 1:
                variable = columns[0].variable_factory()
                for values in result:
                    result.set_variable(variable, values[0])
                    yield variable.get()
            else:
                variables = [column.variable_factory() for column in columns]
                for values in result:
                    for variable, value in zip(variables, values):
                        result.set_variable(variable, value)
                    yield tuple(variable.get() for variable in variables)
        except Exception as db_error:
            if db_error[0].code == RESOURCE_BUSY_ERROR_CODE:  # Resource busy
                raise DatabaseResourceBusyException(_(RESOURCE_BUSY_ERROR_MESSAGE))

            raise db_error


Store._result_set_factory = DeltaResultSet


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


    def execute(self, statement, params=None, noresult=False):
        """Execute a basic query.

        This is just like L{storm.database.Database.execute}, except
        that a flush is performed first.
        """
        try:
            return super(TransactionalStore, self).execute(statement, params, noresult)
        except Exception as db_error:
            #if db_error[0].code == RESOURCE_BUSY_ERROR_CODE:  # Resource busy
            #    raise DatabaseResourceBusyException(_(RESOURCE_BUSY_ERROR_MESSAGE))

            raise

    def get(self, cls, key, **options):
        """Get object of type cls with the given primary key from the database.

        If the object is alive the database won't be touched.

        @param cls: Class of the object to be retrieved.
        @param key: Primary key of object. May be a tuple for composed keys.

        @return: The object found with the given primary key, or None
            if no object is found.
        """
        for_update_nowait = options.get("for_update_nowait")

        if for_update_nowait is not True:
            for_update_nowait = False

        if self._implicit_flush_block_count == 0:
            self.flush()

        if type(key) != tuple:
            key = (key,)

        cls_info = get_cls_info(cls)

        assert len(key) == len(cls_info.primary_key)

        primary_vars = []
        for column, variable in zip(cls_info.primary_key, key):
            if not isinstance(variable, Variable):
                variable = column.variable_factory(value=variable)
            primary_vars.append(variable)

        primary_values = tuple(var.get(to_db=True) for var in primary_vars)
        obj_info = self._alive.get((cls_info.cls, primary_values))
        if obj_info is not None and not obj_info.get("invalidated"):
            return self._get_object(obj_info)

        where = compare_columns(cls_info.primary_key, primary_vars)

        select = Select(cls_info.columns, where,
                        default_tables=cls_info.table,
                        limit=1,
                        for_update_nowait=for_update_nowait)
        try:
            result = self._connection.execute(select)
        except Exception as db_error:
            if db_error[0].code == RESOURCE_BUSY_ERROR_CODE:  # Resource busy
                raise DatabaseResourceBusyException(_(RESOURCE_BUSY_ERROR_MESSAGE))

            raise db_error

        values = result.get_one()
        if values is None:
            return None
        return self._load_object(cls_info, result, values)

    def find(self, cls_spec, *args, **kwargs):
        """Perform a query.

        Some examples::

            store.find(Person, Person.name == u"Joe") --> all Persons named Joe
            store.find(Person, name=u"Joe") --> same
            store.find((Company, Person), Person.company_id == Company.id) -->
                iterator of tuples of Company and Person instances which are
                associated via the company_id -> Company relation.

        @param cls_spec: The class or tuple of classes whose
            associated tables will be queried.
        @param args: Instances of L{Expr}.
        @param kwargs: Mapping of simple column names to values or
            expressions to query for.

        @return: A L{ResultSet} of instances C{cls_spec}. If C{cls_spec}
            was a tuple, then an iterator of tuples of such instances.
        """
        for_update_nowait = kwargs.pop('for_update_nowait', False)
        if self._implicit_flush_block_count == 0:
            self.flush()
        find_spec = FindSpec(cls_spec)
        where = get_where_for_args(args, kwargs, find_spec.default_cls)
        return self._result_set_factory(self, find_spec, where,
                                        for_update_nowait=for_update_nowait)
