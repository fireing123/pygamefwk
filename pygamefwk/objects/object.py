from pygamefwk.manger import Manger
from pygamefwk.objects.component import Component


class Object(Component):
    def __init__(self, name, layer, tag):
        self.name = name
        self.tag = tag
        self.layer = layer
        self.components : list[Component] = []

    def delete(self): 
        """씬에서 이 오브젝트를 삭제합니다"""
        try:
            for component in self.components:
                component.delete()
                
            Manger.scene.remove(self)
        except: pass
        del self

    def init_instantiate(self):
        Manger.scene.add(self)