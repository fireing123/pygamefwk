from pygamefwk.objects.gameobject import GameObject

class MapCenter(GameObject):
    """아무 기능없는 그냥 오브젝트이지만,
    상대좌표로 표기하는 position을 사용해 위치 표기를 더욱 좋게 표기함"""
    def __init__(self, name, position, parent_name):
        super().__init__(name, 1, "parent", True, position, 0, parent_name)