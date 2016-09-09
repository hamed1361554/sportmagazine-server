'''
Created on Sep 5, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import threading

class SetterTrigger:
    """
    Trigger class notifies any property change of given delta object.    
    """
    def __init__(self, name, obj, trigger_func):
        """
        class initialization.
        @param name: trigger name or key.
        @param obj: object that should be triggered.
        @param trigger_func: a function that  trigger will called it on each change.
        """
        if not hasattr(obj,'setattr'):
            raise Exception("Object[%s] must have 'setattr' method." % obj)
        
        self.obj = obj
        if not hasattr(self.obj,'orginal_setattr'):
            self.obj.orginal_setattr = obj.setattr
        if not hasattr(self.obj, 'triggers'):
            self.obj.triggers = []
        self.obj.triggers.append(self)
        self.trigger_func = trigger_func        
        self.enabled = False
        self.prev_setattr = None
        self.name = name
        self.id = id(self)
        self._lock = threading.Lock()
    
    #def __del__(self):
    #    """
    #    destructor of class.
    #    """
    #    self.__detach()
    
    def refresh(self):
        """
        it refreshes trigger states. 
        """
        if self.prev_setattr and self.prev_setattr != self.obj.setattr:
            self.prev_setattr = self.obj.setattr
    
    def __refresh_obj_triggers(self):
        """
        refreshes all attached triggers and refactors all private function references.
        """
        try:
            self._lock.acquire()
            prev_setattr = self.obj.orginal_setattr
            self.obj.setattr = self.obj.orginal_setattr
            for trg in self.obj.triggers:
                if trg.enabled:
                    trg.prev_setattr = prev_setattr
                    self.obj.setattr = trg.__on_setattr
                    prev_setattr = self.obj.setattr 
                else:
                    trg.prev_setattr = None
        finally:
            self._lock.release()
            
    def __detach(self):
        """
        it detaches trigger functions.
        """
        try:
            self._lock.acquire()
            self.disable()
            self.obj.triggers.remove(self)
            self.__refresh_obj_triggers()
        finally:
            self._lock.release()
        
    def enable(self):
        """
        enables trigger.
        """
        if not self.enabled:
            self.enabled = True
            self.__refresh_obj_triggers()
        print "trigger[%s] enabled." % self
    
    def disable(self):
        """
        disables trigger.
        """
        if self.enabled:
            self.enabled = False
            self.__refresh_obj_triggers()
        print "trigger[%s] disabled." % self

    def __on_setattr(self, name, value):
        """
        internal replacement set attribute function.
        """
        if self.prev_setattr:
            old_value = getattr(self.obj, name, value)
            if self.trigger_func(self.obj, name, old_value, value) == False:
                return
            return self.prev_setattr(name, value)
    
    def __repr__(self):
        """
        introduce method.
        """
        return self.name    
