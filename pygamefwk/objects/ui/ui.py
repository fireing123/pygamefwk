from pygamefwk.objects.gameobject import GameObject

class UI(GameObject):
    """ui 를 위한 오브젝트"""
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)