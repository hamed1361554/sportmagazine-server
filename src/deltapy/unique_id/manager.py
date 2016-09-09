'''
Created on Dec 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject, DeltaException

class UniqueIDManagerException(DeltaException):
    '''
    Represent unique ID manager errors.
    '''

class UniqueIDManager(DeltaObject):
    '''
    Unique ID manager class
    '''
    
    def __init__(self):
        DeltaObject.__init__(self)
        
        self._registered_generators = {}
        
    def register_generator(self, name, generator):
        '''
        Registers an unique ID generator.
        
        @param name: generator name
        @param generator: generator instance
        '''
        
        self._registered_generators[name] = generator
        
    def get_generator(self, name):
        '''
        Returns the specific generator by given name.
        
        @param name: generator name
        @return: UniqueIDGenerator
        '''
        
        generator = self._registered_generators.get(name)
        if generator is None:
            message = _('Could not found unique ID generator[{name}].')
            raise UniqueIDManagerException(message.format(name=name))
        return generator

    def get_id(self, generator_name, **options):
        '''
        Returns an unique ID using corresponded registered generator.
        
        @param generator_name: unique ID generator name.
        @param **options: unique ID generator options
        @return: object
        '''
        
        return self.get_generator(generator_name).get(**options)
    
    def put_id(self, generator_name,  id, **options): 
        '''
        Puts the given ID in queue.
        
        @param generator_name: unique ID generator name.
        @param id: particular ID
        @param **options:
        '''

        return self.get_generator(generator_name).put(id, **options)
    
    def reserve_id(self, generator_name, id, **options): 
        '''
        Reserves the given ID.
        
        @param generator_name: unique ID generator name.
        @param id: particular ID
        @param **options:
        '''
        
        return self.get_generator(generator_name).reserve(id, **options)

    def refresh(self, generator_name, **options):
        '''
        Refreshes the unique ID generator. 
        
        @param generator_name: unique ID generator name.
        @param **options: unique ID generator options
        '''
        
        self.get_generator(generator_name).refresh()
