'''
Created on Oct 12, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

def provides(*interfaces):
    """
    An actual, working, implementation of provides for
    the current implementation of PyProtocols.  Not
    particularly important for the PEP text.

    class IBar(Interface):
         '''Declare something about IBar here'''
    
    @provides(IBar)
    class Foo(object):
            '''Implement something here...'''
    """
    def provides(typ):
        declareImplementation(typ, instancesProvide=interfaces)
        return typ
    return provides
    
    
def accepts(*types):
    '''
    @accepts(int, (int,float))
    @returns((int,float))
    def func(arg1, arg2):
        return arg1 * arg2
    '''
    def check_accepts(f):
        assert len(types) == f.func_code.co_argcount
        def new_f(*args, **kwds):
            for (a, t) in zip(args, types):
                assert isinstance(a, t), \
                       "arg %r does not match %s" % (a,t)
            return f(*args, **kwds)
        new_f.func_name = f.func_name
        return new_f
    return check_accepts

def returns(rtype):
    '''
    @accepts(int, (int,float))
    @returns((int,float))
    def func(arg1, arg2):
        return arg1 * arg2
    '''
    def check_returns(f):
        def new_f(*args, **kwds):
            result = f(*args, **kwds)
            assert isinstance(result, rtype), \
                   "return value %r does not match %s" % (result,rtype)
            return result
        new_f.func_name = f.func_name
        return new_f
    return check_returns

def attrs(**kwds):
    '''
    @attrs(versionadded="2.2",
           author="Guido van Rossum")
    def mymethod(f):
        ...
    '''
    def decorate(f):
        for k in kwds:
            setattr(f, k, kwds[k])
        return f
    return decorate

def singleton(cls):
    '''
    @singleton
    class MyClass:
        ...
    '''
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance




