import base64
from decimal import Decimal
import os
from storm.tracer import trace
from storm.variables import PickleVariable, Variable

__author__ = 'Hamed'

from storm.info import get_cls_info, ClassAlias
from storm.expr import (
    Undef, Expr, SetExpr, Select, Insert, Alias, And, Eq, FuncExpr, SQLRaw,
    Le, Gt, Column, EXPR, Except,
    SQLToken, COLUMN, COLUMN_NAME, COLUMN_PREFIX, TABLE,
    compile, compile_select, compile_insert, compile_set_expr, compile_sql_token, compile_python, Mod, In)
from storm.database import Database, Connection, Result, convert_param_marks


@compile.when(type)
def compile_type(compile, expr, state):
    cls_info = get_cls_info(expr)
    table = compile(cls_info.table, state)
    if state.context is TABLE and issubclass(expr, ClassAlias):
        return "%s %s" % (compile(cls_info.cls, state), table)
    return table

@compile.when(Alias)
def compile_alias(compile, alias, state):
    name = compile(alias.get_name(state), state, token=True)
    if state.context is COLUMN or state.context is TABLE:
        return "%s %s" % (compile(alias.expr, state), name)
    return name

@compile.when(SQLToken)
def compile_sql_token_oracle(compile, expr, state):
    # this is a simple hack to make sure all auto-generated aliases
    # get escaped; I added this if because oracle was complaining of
    # stuff such as money."value", that was being generated;
    if state.context in (TABLE, COLUMN_PREFIX, COLUMN, COLUMN_NAME, EXPR):
        if expr.startswith('_'):
            return '"%s"' % (expr)
        return expr

    if "." in expr and state.context in (TABLE, COLUMN_PREFIX):
        return ".".join(compile_sql_token(compile, subexpr, state)
                        for subexpr in expr.split("."))
    return compile_sql_token(compile, expr, state)

class Minus(SetExpr):
    oper = " MINUS "

@compile.when(Except)
def compile_except_oracle(compile, expr, state):
    new_expr = Minus()
    new_expr.exprs = expr.exprs
    new_expr.all = expr.all
    new_expr.order_by = expr.order_by
    new_expr.limit = expr.limit
    new_expr.offset = expr.offset
    return compile_set_expr_oracle(compile, new_expr, state)

@compile.when(SetExpr)
def compile_set_expr_oracle(compile, expr, state):
    if isinstance(expr, Minus):
        # Build new set expression without arguments (order_by, etc).
        new_expr = expr.__class__()
        new_expr.exprs = expr.exprs
        new_expr.all = expr.all

        if expr.order_by is not Undef:
            # Make sure that state.aliases isn't None, since we want them to
            # compile our order_by statement below.
            no_aliases = state.aliases is None
            if no_aliases:
                state.push("aliases", {})

            aliases = {}
            for subexpr in expr.exprs:
                if isinstance(subexpr, Select):
                    columns = subexpr.columns
                    if not isinstance(columns, (tuple, list)):
                        columns = [columns]
                    else:
                        columns = list(columns)
                    for i, column in enumerate(columns):
                        if column not in aliases:
                            if isinstance(column, Column):
                                aliases[column] = columns[i] = Alias(column)
                            elif isinstance(column, Alias):
                                aliases[column.expr] = column
                    subexpr.columns = columns
            aliases.update(state.aliases)
            state.aliases = aliases
            aliases = None

        set_stmt = SQLRaw('(%s)' % compile(expr.exprs, state, join=expr.oper))

        if expr.order_by is not Undef:
            # Build order_by statement, using aliases.
            state.push("context", COLUMN_NAME)
            order_by_stmt = SQLRaw(compile(expr.order_by, state))
            state.pop()
        else:
            order_by_stmt = Undef

        # Build wrapping select statement.
        select = Select(SQLRaw("*"), tables=Alias(set_stmt), limit=expr.limit,
                        offset=expr.offset, order_by=order_by_stmt)

        return compile_select(compile, select, state)
    return compile_set_expr(compile, expr, state)

@compile.when(Select)
def compile_select_oracle(compile, select, state):
    limit = select.limit
    offset = select.offset
    # make sure limit is Undef'ed
    select.offset = select.limit = Undef

    if select.default_tables is Undef:
        select.default_tables = ['DUAL']

    if select.order_by is not Undef:
        # copied from expr.py's compile_set_expr
        aliases = {}
        columns = select.columns
        if not isinstance(columns, (tuple, list)):
            columns = [columns]
        else:
            columns = list(columns)
        for i, column in enumerate(columns):
            if column not in aliases:
                if isinstance(column, Column):
                    aliases[column] = columns[i] = Alias(column)
                elif isinstance(column, Alias):
                    aliases[column.expr] = column
        select.columns = columns
        # /copied from expr.py's compile_set_expr
        stmt = SQLRaw("(%s)" % compile_select(compile, select, state))
        stmt_alias = Alias(stmt)
        # In order to force the alias to generate its auto-name.
        stmt_alias.get_name(state)
        select = Select(SQLRaw('*'), tables=stmt_alias)

    if (limit is not Undef) and (offset is not Undef):
        rownum_alias = Alias(SQLRaw('ROWNUM'))

        # if we have an SQLRaw here that is because we are dealing
        # with a subquery
        if isinstance(select.columns, SQLRaw):
            select.columns = [SQLRaw('"' + select.tables.name + '".*'), rownum_alias]
        else:
            select.columns.append(rownum_alias)

        where_expr = Le(SQLRaw('ROWNUM'), limit + offset)
        if select.where is Undef:
            select.where = where_expr
        else:
            select.where = And(select.where, where_expr)

        stmt = SQLRaw("(%s)" % compile_select(compile, select, state))
        stmt_alias = Alias(stmt)
        # In order to force the alias to generate its auto-name.
        stmt_alias.get_name(state)
        select = Select(SQLRaw('*'), tables=stmt_alias, where = Gt(rownum_alias, offset))
    elif limit is not Undef:
        expr = Le(SQLRaw('ROWNUM'), limit)
        if select.where is Undef:
            select.where = expr
        else:
            select.where = And(select.where, expr)
    elif offset is not Undef:
        rownum_alias = Alias(SQLRaw('ROWNUM'))

        # if we have an SQLRaw here that is because we are dealing
        # with a subquery
        if isinstance(select.columns, SQLRaw):
            select.columns = [SQLRaw('"' + select.tables.name + '".*'), rownum_alias]
        else:
            select.columns.append(rownum_alias)

        stmt = SQLRaw("(%s)" % compile_select(compile, select, state))
        stmt_alias = Alias(stmt)
        # In order to force the alias to generate its auto-name.
        stmt_alias.get_name(state)
        select = Select(SQLRaw('*'), tables=stmt_alias, where = Gt(rownum_alias, offset))

    return compile_select(compile, select, state)

@compile.when(Insert)
def compile_insert_oracle(compile, insert, state):
    # shamelessly copied from PostgreSQL
    if not insert.map and insert.primary_columns is not Undef:
        insert.map.update(dict.fromkeys(insert.primary_columns,
                                        SQLRaw("DEFAULT")))
    return compile_insert(compile, insert, state)

class currval(FuncExpr):

    name = "currval"

    def __init__(self, column):
        self.column = column

@compile.when(currval)
def compile_currval(compile, expr, state):
    """Compile a currval.
    """
    state.push("context", COLUMN_PREFIX)
    table = compile(expr.column.table, state, token=True)
    state.pop()
    return "%s_seq.currval" % (table)

class Rowid(Expr):
    def __init__(self, rowid):
        self.rowid = rowid

@compile.when(Rowid)
def compile_rowid(compile, expr, state):
    state.parameters.append(expr.rowid)
    return "?"

@compile.when(Mod)
def compile_mode(compile, expr, state):
    expr1 = compile(expr.expr1, state)
    state.precedence = 0 # We're forcing parenthesis here.
    compiled = compile(expr.expr2, state)
    return 'MOD({0}, {1})'.format(expr1, compiled)

@compile.when(In)
def compile_in(compile, expr, state):
    expr1 = compile(expr.expr1, state)
    state.precedence = 0 # We're forcing parenthesis here.
    compiled = compile(expr.expr2, state)
    if isinstance(expr.expr2, (list, tuple)) and isinstance(expr.expr2[0], (list, tuple)) and len(expr.expr2):
        item_len = len(expr.expr2[0])
        index = 0
        new_compiled = ''
        for c in compiled:
            if c == ',':
                index += 1
                if index > 0 and index % item_len == 0:
                    new_compiled += '),('
                else:
                    new_compiled += c
            else:
                new_compiled += c
        compiled = '({0})'.format(new_compiled)

    return "({0}) IN ({1})".format(expr1, compiled)

@compile_python.when(In)
def compile_in_python(compile, expr, state):
    expr1 = compile(expr.expr1, state)
    state.precedence = 0 # We're forcing parenthesis here.
    compiled = compile(expr.expr2, state)
    if isinstance(expr.expr2, (list, tuple)) and isinstance(expr.expr2[0], (list, tuple)) and len(expr.expr2):
        item_len = len(expr.expr2[0])
        index = 0
        new_compiled = ''
        for c in compiled:
            if c == ',':
                index += 1
                if index > 0 and index % item_len == 0:
                    new_compiled += '),('
                else:
                    new_compiled += c
            else:
                new_compiled += c
        compiled = '({0})'.format(new_compiled)

    return "({0}) IN ({1})".format(expr1, compiled)

class MockResult(Result):

    def __init__(self, connection, raw_cursor, rowid=None):
        super(MockResult, self).__init__(connection, raw_cursor)
        self.lastrowid = rowid

    def get_insert_identity(self, primary_key, primary_variables):
        return Eq(Column('rowid'), Rowid(self.lastrowid))

    @staticmethod
    def set_variable(variable, value):
        if isinstance(value, str) and isinstance(variable, PickleVariable):
            value = base64.decodestring(value)
        if isinstance(value, float):
            value = Decimal(repr(value))
        variable.set(value, from_db=True)

    @staticmethod
    def from_database(row):
        """Convert Oracle-specific datatypes to "normal" Python types.

        If there are anny C{buffer} instances in the row, convert them
        to strings.
        """
        for value in row:
            yield value

class MockConnection(Connection):
    result_factory = MockResult
    compile = compile
    param_mark = ":1"

    def execute(self, statement, params=None, noresult=False):
        """NOTE: this is being overriden completely because the
        original from the base class expects to receive only a
        raw_cursor from raw_execute, and we need to receive also the
        rowid, as we cannot set it in the cursor object

        Execute a statement with the given parameters.

        @type statement: L{Expr} or C{str}
        @param statement: The statement to execute. It will be
            compiled if necessary.
        @param noresult: If True, no result will be returned.

        @raise DisconnectionError: Raised when the connection is lost.
            Reconnection happens automatically on rollback.

        @return: The result of C{self.result_factory}, or None if
            C{noresult} is True.
        """
        self._ensure_connected()
        if isinstance(statement, Expr):
            if params is not None:
                raise ValueError("Can't pass parameters with expressions")
            state = None
            statement = self.compile(statement, state)
            params = state.parameters
        statement = convert_param_marks(statement, "?", self.param_mark)
        raw_cursor, rowid = self.raw_execute(statement, params)
        if noresult:
            self._check_disconnect(raw_cursor.close)
            return None
        return self.result_factory(self, raw_cursor, rowid)

    def raw_execute(self, statement, params):
        """NOTE: this is being overriden completely because the original
        from the base class converts params to a tuple, and we need a dictionary!

        Execute a raw statement with the given parameters.

        It's acceptable to override this method in subclasses, but it
        is not intended to be called externally.

        If the global C{DEBUG} is True, the statement will be printed
        to standard out.

        @return: The dbapi cursor object, as fetched from L{build_raw_cursor}.
        """
        rowid = None
        raw_cursor = self.build_raw_cursor()

        # newer cx_Oracle (>= 4.4) seems to really want str() instead
        # of unicode()
        statement = str(statement)

        if statement.startswith('INSERT INTO'):
            statement = statement + ' RETURNING ROWID INTO :out_rowid'

            # make sure params is a list; if it is a tuple we're screwed =)
            if params is None:
                params = list()
            elif not isinstance(params, list):
                params = list(params)

        if params:
            params = self.to_database(params)
            args = (statement, params)
        else:
            args = (statement,)

        user_tracer_data = {}

        trace("connection_raw_execute", self, raw_cursor,
              statement, params or (), user_tracer_data)

        try:
            self._check_disconnect(raw_cursor.execute, *args)
            if rowid:
                rowid = rowid.getvalue()
        except Exception, error:
            trace("connection_raw_execute_error", self, raw_cursor,
                  statement, params or (), user_tracer_data, error)
            raise
        else:
            trace("connection_raw_execute_success", self, raw_cursor,
                  statement, params or (), user_tracer_data)
        return raw_cursor, rowid

    @staticmethod
    def to_database(params):
        """
        Like L{Connection.to_database}, but returns a dictionary.

        params is a list of 1-item dictionaries, which must be merged
        into one big dictionary here; we also need to take care of
        stuff such as cx_Oracle not wanting to receive unicode, and
        converting eventual unicode's to UTF-8 strings
        """
        new_params = []

        for param in params:
            if isinstance(param, Variable):
                value = param.get(to_db=True)
            else:
                value = param

            if isinstance(value, unicode):
                value = value.encode("UTF-8")
            #if isinstance(value, str):
                #value = utf8_to_db_encoding(value)
            #elif isinstance(value, str) and isinstance(variable, PickleVariable):
            elif isinstance(value, PickleVariable):
                value = base64.encodestring(value)

            new_params.append(value)
        return new_params

class Mock(Database):

    connection_factory = MockConnection

    def __init__(self, uri):
        isolation = uri.options.get("isolation", "serializable")
        isolation_mapping = {
            "serializable": 'SERIALIZABLE',
            "read-committed": 'READ COMMITTED',
        }
        try:
            self._isolation = isolation_mapping[isolation]
        except KeyError:
            raise ValueError(
                "Unknown serialization level %r: expected one of "
                "'autocommit', 'serializable', 'read-committed'" %
                (isolation,))

        self._username = uri.username
        self._password = uri.password

    def raw_connect(self):
        return MockConnection()

create_from_uri = Mock