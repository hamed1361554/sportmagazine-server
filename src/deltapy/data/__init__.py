
class PrimaryKey:
    def __init__(self, *args):
        self._pk = args
        
    def __call__(self):
        return self._pk