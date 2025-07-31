import pygame
from pygame import display
from typing import Callable

from pygamefwk.manger        import Manger
from pygamefwk.scene         import Scene
from pygamefwk.mouse         import mouse_event
from pygamefwk.instantiate   import import_module
from pygamefwk.input         import Input
from pygamefwk.event         import Event
from pygamefwk.objects.components.reset import on_reset

import pygamefwk.mouse as mouse

def world(world_path: str):
    """함수를 새상으로 등록하는 데코레이터
    
    Args:
        world_path (str) : json (맵) 경로
    """
    def real_world(func):
        def wrapper(*args):
            Manger.scene = Scene() # 초기화
            on_reset.invoke()
            Manger.scene.load(world_path) # 맵 불러오기
            start, event, update = func(*args)
            Manger.scene.start()
            start()
            reson = Game.loop(event, update)
            del Manger.scene
            return reson
        return wrapper
    return real_world

event_event = Event()

class Game:
    """게임 엔진"""
    
    @classmethod
    def init(cls, size : tuple[int, int], title : str):
        """게임에 초기 설정

        Args:
            size (tuple[int, int]): 스크린 크기
            title (str): 프로그램에 제목
        """
        pygame.init()
        display.set_caption(title)
        pygame.key.start_text_input()
        Manger.init(display.set_mode(size, pygame.DOUBLEBUF, 32), Scene())
    
    @classmethod
    def import_objects(cls, obj_dir : str, **kwargs):
        """클래스들을 불러와 Manger 에 저장합니다

        Args:
            obj_dir (str): 오브젝트 클래스에 파일를 저장한 폴더 경로
        """
        Manger.classes.update(import_module(obj_dir, **kwargs))
    
    @classmethod
    def stop(cls, reson):
        """맵 종료
        
        Args:
            reson (str): 종료 사유
        """
        cls.reson = reson
        cls.is_running = False
    
    @classmethod
    def loop(cls, events: Callable, func: Callable):
        """맵 루프

        Args:
            events (Callable): 이벤트
            func (Callable): 업데이트
        """
        cls.is_running = True
        cls.is_time_running = True
        cls.clock = pygame.time.Clock()
        cls.reson = None

        while cls.is_running:
            Manger.delta_time = cls.clock.tick(60) / 1000 # fps를 직접적으로 제한

            # 이벤트 체크 시작
            mouse_pressed = mouse.get_pressed()
            
            for i in range(3):
                mouse_click = Input.mouse_click[i]
                if mouse_pressed[i]: #현재 눌림
                    if mouse_click <= Input.KEYUP:
                        Input.mouse_click[i] = Input.KEYDOWN # 방금 누름
                    else:
                        Input.mouse_click[i] = Input.KEYDOWNING # 계속 누름
                else:
                    if mouse_click >= Input.KEYDOWN:
                        Input.mouse_click[i] = Input.KEYUP # 방금땜
                    else:
                        Input.mouse_click[i] = Input.KEYUPING # 계속
                        
            mouse_event()
            
            for key, value in Input.key_board.items():
                if value == 2:
                    Input.key_board[key] = 3
                elif value == 1:
                    Input.key_board[key] = 0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cls.stop("quit")
                elif event.type == pygame.KEYDOWN:
                    Input.key_board[event.key] = 2
                elif event.type == pygame.KEYUP:
                    Input.key_board[event.key] = 1
                    
                event_event.invoke(event)
                
                events(event)

            # 이벤트 체크 끝

            func()
            
            if cls.is_time_running:
                Manger.scene.update()

                Manger.scene.physics_step()
            
            Manger.scene.render(Manger.screen)

            pygame.display.update()
        return cls.reson