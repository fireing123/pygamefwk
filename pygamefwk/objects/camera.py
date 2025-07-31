from pygame import Surface
from pygamefwk.objects.gameobject import GameObject
from pygamefwk.vector import Vector
from pygamefwk.manger import Manger
from typing import Sequence

class CameraObject(GameObject):
    def __init__(self, name, tag, visible, position, rotation, parent_name):
        super().__init__(name, 0, tag, visible, position, rotation, parent_name)
        self.cam_color = (127, 127, 127)

    def centerXY(self, position: Sequence[float] | Vector):
        centered = Vector(position)
        centered.x += Manger.WIDTH / 2
        centered.y -= Manger.HEIGHT / 2
        return centered

    def __call__(self, position: Sequence[float] | Vector):
        """카메라 시선을 적용한 위치를 반환함

        Args:
            position (tuple[float, float] | Vector): 오브젝트에 위치

        Returns:
            tuple[float, float]: 카메라 시선이 적용된 위치
        """
        camerad = Vector(position)
        rend = self.location.world_position.copy()
        rend.y = Manger.HEIGHT - rend.y # y 좌표만 반전
        camerad = camerad - rend
        camerad.x += Manger.WIDTH / 2 # 0,0 좌표를 프로그램 중앙으로 설정정
        camerad.y += Manger.HEIGHT / 2
        return camerad

    def render(self, surface: Surface, camera):
        surface.fill(self.cam_color) # background render