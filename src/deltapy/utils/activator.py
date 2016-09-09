'''
Created on Sep 14, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''
    
def get_all_types(module):
    m = __import__(module, fromlist = [])
    return m.__dict__.values()

def get_types(module, base_type):
    m = __import__(module, fromlist = [])
    results = []
    for cls in m.__dict__.values():
        try:
            if cls is not base_type and issubclass(cls, base_type):
                results.append(cls)
        except:
            pass        
    return results

def get_type(module, type_name):
    m = __import__(module, fromlist = [])        
    for cls in m.__dict__.values():
        try:
            if cls.__name__ == type_name:
                return cls
        except:
            pass
        
    return None

def create_instance(type, *params):
    return type(*params)

def create_instance_by_name(module ,type_name, *params):
    typ = get_type(module,type_name)
    if typ:
        return typ(*params)
    return None
