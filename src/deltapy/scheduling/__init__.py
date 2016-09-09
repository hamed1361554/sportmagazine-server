from deltapy.packaging.package import Package

class SchedulingPackage(Package):
    
    __depends__ = ['deltapy.config', 'deltapy.logging', 'deltapy.commander', 'deltapy.transaction']
    
        
        
