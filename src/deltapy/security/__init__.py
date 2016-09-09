from deltapy.packaging.package import Package

PERMISSION_HOLDER = 'security.permission_holder'

class SecurityPackage(Package):
    
    __depends__ = ['deltapy.config', 
                   'deltapy.logging', 
                   'deltapy.commander', 
                   'deltapy.database', 
                   'deltapy.transaction',
                   'deltapy.unique_id']

