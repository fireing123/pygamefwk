import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygamefwk.objects.camera import CameraObject

class Component:
    """기본 함수만 선언해놓음"""
    def on_mouse_enter(self, pos: tuple[int, int]):
        """마우스가 오브젝트(rect) 안에 들어올떄 호출됨

        Args:
            pos (tuple[int, int]): 마우스 위치 (접촉한 위치)
        """
        ...
        
    def on_mouse_stay(self, pos: tuple[int, int]):
        """마우스가 오브젝트(rect) 에서 들어온 상태일떄 계속 호출됨

        Args:
            pos (tuple[int, int]): 마우스 위치 (접촉한 위치)
        """
        ...
    def on_mouse_exit(self, pos: tuple[int, int]):
        """마우스가 오브젝트(rect) 에서 들어온 상태였다가 나오면 호출됨

        Args:
            pos (tuple[int, int]): 마우스 위치 (접촉한 위치)
        """
        ...
    def start(self):
        """오브젝트가 전부 생성된 후에 실행됨"""
        ...
    def update(self):
        """게임 루프시 한번씩 실행됩니다"""
        ...
    def render(self, surface: pygame.Surface, camera: 'CameraObject'):
        """씬에서 그릴때 실행합니다

        Args:
            surface (pygame.Surface): 프로그램 화면
            camera (Camera): 씬 카메라
        """
        ...
    def delete(self): ...

    def child_instantiate(self):...