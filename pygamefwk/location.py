from pygamefwk import Vector
from typing import List, TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from pygamefwk.objects.gameobject import GameObject

class Parent:
    def __init__(self, object: 'GameObject'):
        self.object = object
        self.visible = True
        self.world_visible = True
        self.position = Vector(0, 0)
        self.world_position = Vector(0, 0)
        self.rotation = 0
        self.world_rotation = 0
        self.children: List['Location'] = []

    def set_world(self):
        for child in self.children:
            child.change_location()

class Location:
    """위치, 각도, visible 부모 자식 관계를 형성, 위치, 각도를 상대적으로 만듬"""
    def __init__(self, object: 'GameObject', position: Vector, rotation: int, visible: bool):
        self.object = object
        self.__visible: bool = visible
        self.__position = Vector(position)
        self.__rotation: int = rotation
        self.__world_position = Vector(0, 0)
        self.__world_rotation = 0
        self.__world_visible = False
        self.parent : Parent = None
        self.children: List['Location'] = []

    def translate(self, vector: Vector):
        self.position += vector

    def set_parent(self, parent: Parent):
        self.parent = parent
        parent.children.append(self)
    
    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, value: bool):
        self.__visible = value
        self.change_location()

    @property
    def position(self):
        return self.__position
    
    @position.setter
    def position(self, vector: Sequence):
        self.__position = Vector(vector)
        self.change_location()

    @property
    def rotation(self):
        return self.__rotation
    
    @rotation.setter
    def rotation(self, degree: int):
        if degree > 360:
            degree = degree // 360
        self.__rotation = degree
        self.change_location()
        
    @property
    def world_position(self):
        return self.__world_position
    
    @property
    def world_rotation(self):
        return self.__world_rotation
    
    @property
    def world_visible(self):
        return self.__world_visible

    def change_location(self):
        """상위 오브젝트의 Location 정보가 갱신되거나 객체의 정보가 변경되면 world_XXX 를 업데이트 하기 위해 정해짐"""
        self.__world_position: Vector = self.parent.world_position + self.__position.rotate(self.parent.rotation)
        self.__world_rotation: int = self.parent.world_rotation + self.__rotation
        self.__world_visible: bool = self.visible and self.parent.world_visible
        for child in self.children:
            child.change_location()