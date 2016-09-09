from deltapy.packaging.package import Package
from deltapy.locals import *
from deltapy.scripting.manager import ScriptManager

class ScriptingPackage(Package):
    
    __depends__ = ['deltapy.config', 'deltapy.logging', 'deltapy.commander']

    def load(self):
        Package.load(self)
        get_app_context()[APP_SCRIPTING] = ScriptManager()
        
        
        
