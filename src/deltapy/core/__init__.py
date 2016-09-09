'''
@author: abi m.s, majid v.a
'''

class DeltaException(Exception):
    '''
    Base class for this application engine exceptions.
    '''
    
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        
        self._data = {}
        
    def get_code(self):
        '''
        Returns error code.
        '''
        
        return self.__class__.__name__
    
    def get_data(self):
        '''
        Returns error data.
        '''
        
        return self._data

class DeltaObject(object):
    '''
    Base class for all classes in deltapy framework.
    '''
    def __init__(self):
        '''
        The constructor method.
        '''
        object.__init__(self)
        self.__name = None

    def get_name(self):
        '''
        Returns the name of the object.
        
        @return: str
        '''
        
        if self.__name:
            return self.__name
        return self.__class__.__name__
    
    def _set_name_(self, name):
        '''
        Sets new name to current object.
        @param name: object name
        '''
        self.__name = name
        
    def get_doc(self):
        '''
        Returns doc of the object.
        
        @return: str
        '''
        
        return self.__doc__

    def setattr(self, name, value):
        """
        set attribute function.
        """
        return object.__setattr__(self, name, value)
        
    def __setattr__(self, name, value):
        """
        overriding internal __setattr__
        """
        return self.setattr(name, value)        

class DynamicObject(dict):
    '''
    The context class for storing objects in every layers.
    '''
    
    def __getattr__(self, name):
        if self.has_key(name):
            return self.get(name)
        raise AttributeError('Property[%s] not found.' % name)
    
    def __setattr__(self, name, value):
        self[name] = value
        
    def __hash__(self):
        return hash(tuple(self.values()))
    
    def __eq__(self, other):
        if not other or not isinstance(other, DynamicObject):
            return False
        keys = self.keys()
        if len(keys) != len(other.keys()):
            return False
        for key in keys:
            if self.get(key, None) != other.get(key, None):
                return False
        return True
    
    def __getstate__(self):
        '''
        '''
        pass
    
    def __setstate__(self, (keys, values)):
        '''
        '''
        pass
        
   
class ContextException(DeltaException):
    '''
    Context exception class.
    '''
    pass

class Context(DynamicObject):
    '''
    The context class for storing objects in every layers.
    '''
        
    def __setattr__(self, name, value):
        if self.has_key(name):
            self[name] = value
        raise ContextException('Property[%s] not found.' % name)
    
class DeltaEnumValue:
    def __init__(self, value, description):
        self.value = value
        self.description = description
    def __str__(self):
        return self.description
    def __eq__(self, other):
        if isinstance(other, DeltaEnumValue):
            return self.value == other.value
        return self.value == other
    def __repr__(self):
        return self.description
    
class DeltaEnum:
    class __metaclass__(type):
        def __getattribute__(self, name):
            property = type.__getattribute__(self, name)
            if isinstance(property, DeltaEnumValue):
                return property.value
            return property
    
    @classmethod
    def str(cls, value):
        '''
        Returns string of enumeration value.

        @param self: class 
        @param value: value
        '''
        for property in cls.__dict__.values():
            if isinstance(property, DeltaEnumValue):
                if property.value == value:
                    return str(property)
        raise Exception('Enum [{classname}] has not value [{value}]'.format(value=value, classname=cls.__name__))

    @classmethod
    def to_dictionary(cls):
        '''
        Returns a DynamicObject that contains all
        of the items deifined in this enumeration.

        @return: DynamicObject<value, description>
        '''
        result = DynamicObject()
        for property in cls.__dict__.values():
            if isinstance(property, DeltaEnumValue):
                result[property.value] = property.description
        return result

    @classmethod
    def contains(cls, key):
        '''
        Returns True if `key' exists in the enumartion.
        Returns False otherwise.

        @param key: Key to search in enumeration.

        @return: Boolean
        '''
        for property in cls.__dict__.values():
            if isinstance(property, DeltaEnumValue):
                if property.value == key:
                    return True
        return False

def enum_to_string(enum, value):
    return enum.str(value)

