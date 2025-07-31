import pygame
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from pygamefwk.scene import Scene
    from pygamefwk.sheet import SurfaceSheet, TileSheet

class Manger:
    """정적 변수를 이곳에 저장함"""
    
    classes = {}
    obj_names = []
    delta_time: float
    tile_sheet: Dict[str, 'TileSheet']
    surface_sheet: Dict[str, 'SurfaceSheet']

    @classmethod
    def init(cls, screen: pygame.Surface, none_scene: 'Scene'):
        """게임에 정적 변수 초기 설정 함수

        Args:
            screen (pygame.Surface): 프로그램 스크린
            none_scene (Scene): 맵
        """
        cls.screen = screen
        cls.scene = none_scene
        cls.WIDTH, cls.HEIGHT = screen.get_size()