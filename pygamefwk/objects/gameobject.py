from pygamefwk import util
from pygamefwk.location import Location
from pygamefwk.manger import Manger
from pygamefwk.objects.object import Object
from pygamefwk.vector import Vector
from collections import deque

class GameObject(Object):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag)
        self.location = Location(self, Vector(*position), rotation, visible)
        self.parent_name = parent_name
        self.childrens = deque()

    @util.getter
    def render_position(self):
        """프로그램창은 Y좌표가 상반되기에 y좌표를 반전시키는"""
        render_pos = Vector(self.location.world_position.x,  Manger.HEIGHT - self.location.world_position.y)
        return render_pos
    
    def delete(self):
        for child in self.location.children:
            child.object.delete()
        return super().delete()

    def instantiate(self):
        """동적 생성으로 게임이 시작된 이후 실행할떈
        이 함수를 사용해야한다"""
        self.init_instantiate(True)
        self.set_parent()
        self.location.change_location()
        for component in self.components:
            component.start()
        self.start()

    def init_instantiate(self, running=False):
        """게임을 로딩할때 실행되는 함수
        만약 자식 오브젝트를 부모보다 먼저 실행되게 하려면
        children.append(children) 대신 children.init_instantiate() 를 실행하세요"""
        super().init_instantiate()
        self.child_instantiate(running)

    def child_instantiate(self, running=False):
        while self.childrens:
            child: 'GameObject' = self.childrens.popleft()
            if running:
                child.instantiate()
            else:
                child.init_instantiate()

    def set_parent(self):
        """부모 객체와 연결"""
        parent: 'GameObject' = Manger.scene.get_object(self.parent_name)
        self.location.set_parent(parent.location)

    def set_child(self, child):
        self.location.children.append(child)