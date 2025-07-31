from pygamefwk.objects.object import Object
from pygamefwk.location import Parent

class ParentObject(Object):
    def __init__(self):
        super().__init__("parent", 0, "parent")
        self.visible = False
        self.location = Parent(self)
        
    def set_parent(self):
        pass