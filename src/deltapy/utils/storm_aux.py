'''
Created on Aug 2, 2009

@author: mohammadi, vesal
'''

from storm.references import BoundReferenceSet, BoundIndirectReferenceSet
from storm.locals import Storm
from storm.info import get_cls_info, get_obj_info, set_obj_info
from storm import Undef

#__cache__ = {}
#
#def get_members(obj):
#    if __cache__.has_key(obj.__class__):
#        return __cache__[obj.__class__]
#    members = []
#    for o in dir(obj):
#        if not o.startwith('_') and o.__class__.__name__ != 'instancemethod':
#            members.append(o)
#    __cache__[obj.__class__] = members 
#    return members

class UnboundReferenceSet(list):
    """
    A simple class which inherited from list.
    We replace this class with BoundReferenceSet in detached entities. 
    """
    
    def add(self, obj):
        """
        A wrapper on append method of super class.
        """
        return self.append(obj)

def get_entity_pk(entity):
    """
    Returns the primary key of entity in tuple.
    
    @entity : Entity object instance.
    @return : The primary key of given entity. 
    """
    
    # Getting object info of entity...
    obj_info = get_obj_info(entity)
    
    values = []
    pk = getattr(entity, '__storm_primary__')
    if type(pk) is not tuple:
        pk = pk,
    for column in pk:
        values.append(getattr(entity, column))
        
    return tuple(values)
    
def __sync_entity__(base, other, synced_cache):
    """
    Synchronizes base entity with other entity.
    
    @param base: base entity which changes will apply on it.
    """
    
    if other is None:
        return
    if not isinstance(base, other.__class__):
        raise Exception('Could not sync %s entity with %s entity.' % (base.__class__, other.__class__))
    if base in synced_cache:
        return
    obj_info = get_obj_info(base)
    for column in obj_info.cls_info.attributes:
        base_value = getattr(base, column)
        other_value = getattr(other, column)
        if base_value != other_value:
            setattr(base, column, other_value)
    synced_cache[base] = True
    for attr in dir(base):
        reference = getattr(base, attr)
        if type(reference) is BoundReferenceSet:
            base_dict = {}
            for child in reference:
                base_dict[get_entity_pk(child)] = child
            other_dict = {}
            for child in getattr(other, attr):
                other_dict[get_entity_pk(child)] = child
            
            # Delete...
            for pk in base_dict:
                if pk not in other_dict:
                    base_entity = base_dict[pk]
                    reference.remove(base_entity)
                    #base_dict.pop(pk)
            
            # Update...
            for pk in base_dict:
                if pk in other_dict:
                    base_entity = base_dict[pk]
                    other_entity = other_dict[pk]
                    __sync_entity__(base_entity, other_entity, synced_cache)
                    #* base_dict.pop(pk)
                    #* other_dict.pop(pk)

            # Adding new records...
            for pk in other_dict:
                if pk not in base_dict:
                    other_entity = other_dict[pk]
                    reference.add(other_entity)                    
            # Insert...
            #* for other_entity in other_dict.values():
            #*    reference.add(other_entity)
            
        if isinstance(reference, Storm):
            __sync_entity__(reference, getattr(other, attr), synced_cache)
            
def sync_entity(base, other):
    obj_cache = {}
    __sync_entity__(base, other, obj_cache)
    del obj_cache
    
def __make_entity_from_dic__(entity_class, dictionary, obj_cache):
    if dictionary is None:
        return None
    
    if id(dictionary) in obj_cache:
        return obj_cache[id(dictionary)]

    entity = entity_class()
    
    obj_info = get_obj_info(entity)
    for o in obj_info.cls_info.attributes:
        setattr(entity, o, dictionary[o])
        
    obj_cache[id(dictionary)] = entity
    for o in dir(entity):
        reference = getattr(entity, o)
        if type(reference) in (BoundReferenceSet,):#, BoundIndirectReferenceSet):
            childs = dictionary[o]
            child_class = reference._target_cls
            reference = UnboundReferenceSet()
            setattr(entity, o, reference)
            for child_dictionay in childs:
                reference.add(__make_entity_from_dic__(child_class, child_dictionay, obj_cache))
        elif isinstance(reference, Storm):
            child_dictionay = dictionary[o]
            setattr(entity, o, __make_entity_from_dic__(reference.__class__, child_dictionay, obj_cache))
    return entity

def __make_dic_from_entity__(entity, deep, exclude, obj_cache):
    if entity is None:
        return None
    
    if deep < 0:
        return None
    
    if entity in obj_cache:
        return obj_cache[entity]
    
    obj_info = get_obj_info(entity)
    obj_tree = {}
    obj_cache[entity] = obj_tree
    
    for o in obj_info.cls_info.attributes:
        obj_tree[o] = getattr(entity, o)

    if deep == 0:
        return obj_tree
    
    for o in dir(entity):
        reference = getattr(entity, o)
        if type(reference) in (BoundReferenceSet,):#, BoundIndirectReferenceSet):
            if o not in exclude:
                childs = []
                for child in reference:
                    childs.append(__make_dic_from_entity__(child, deep - 1, exclude, obj_cache))
                obj_tree[o] = childs
        if isinstance(reference, Storm):
            if o not in exclude:
                obj_tree[o] = __make_dic_from_entity__(reference, deep - 1, exclude, obj_cache)
    return obj_tree

def __detach_entity__(entity, detached_entities):
    if entity in detached_entities:
        return entity

    obj_info = get_obj_info(entity)
    
    if hasattr(obj_info, 'store'):
        store = getattr(obj_info, 'store')
        store._dirty.pop(obj_info, None)
        store._disable_lazy_resolving(obj_info)
        store._disable_change_notification(obj_info)
        store._remove_from_alive(obj_info)
        store._set_clean(obj_info)
        del obj_info["store"]
        
    detached_entities[entity] = True
    
    for o in dir(entity):
        reference = getattr(entity, o)
        if type(reference) is BoundReferenceSet:
            childs = UnboundReferenceSet()
            for child in reference:
                childs.add(__detach_entity__(child, detached_entities))
            setattr(entity, o, childs)
        elif isinstance(reference, Storm):
            setattr(entity, o, __detach_entity__(reference, detached_entities))
        
    for column in obj_info.cls_info.columns:
        variable = obj_info.variables[column]
        variable._lazy_value = Undef
        variable.event = None
            
    return entity
    

def dic_to_entity(entity_class, dictionary):
    obj_cache = {}
    result = __make_entity_from_dic__(entity_class, dictionary, obj_cache)
    del obj_cache
    return result

def entity_to_dic(entity, deep = 0, exclude = []):
    obj_cache = {}
    result = __make_dic_from_entity__(entity, deep, exclude, obj_cache)
    del obj_cache
    return result
    
def object_to_entity(entity_class, obj):
    pass

def entity_to_object(obj_class, entity):
    pass

def attach(store, entity):
    base = store.get(entity.__class__, get_entity_pk(entity))
    
    if not base:
        # Creating a new entity if does not exists in database...
        base = entity.__class__()
        store.add(base)
    
    sync_entity(base, entity)
    
    return base

def detach(entity):
    if not entity:
        return None
    dic = entity_to_dic(entity)
    entity = dic_to_entity(entity.__class__, dic)
    return entity

def get_raw_connection(store):
    """
    get_raw_connection(store) -> connection

    Returns the raw connection of the store object.
    """

    # Getting raw connection of the store...
    return store._connection._raw_connection

def create_raw_cursor(store):
    """
    create_raw_cursor(store) -> cursor

    Creates and returns a raw cursor.
    """

    # Getting raw connection of the store...
    connection = get_raw_connection(store)

    # Creating and returning a raw cursor...
    return connection.cursor()


