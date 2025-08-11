import inspect

import pygame
import pygamefwk.util as _util
from pygamefwk.objects import *
from pygamefwk.objects.components.physics import physics_objects

from pygamefwk.manger import Manger
from pygamefwk.sheet import TileSheet, SurfaceSheet, SpriteSheet

from typing import List, TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from pygamefwk.objects.gameobject import GameObject
    from pygamefwk.objects.camera import CameraObject

class Scene:

    def __init__(self):
        self.layers: List[List['GameObject']] = [[],[],[],[],[],[],[],[],[],[]]
        self.__display = "main_cam"
        self.obj_cache = {}
        self.camera: 'CameraObject'

    def physics_step(self):
        for phyics in physics_objects:
            phyics.step()

    def start(self):
        for layer in self.layers:
            for obj in layer:
                for component in obj.components:
                    component.start()
                obj.start()

    def update(self):
        """등록된 객체에 update 함수를 실행합니다
        """
        for layer in self.layers:
            for obj in layer:
                for component in obj.components:
                    #try:
                    component.update()
                    #except Exception as e:
                    #    print(f"UPDATE {obj.name} components name: {component.__class__} error {e}")
                #try:
                obj.update()
                #except Exception as e:
                #    print(f"UPDATE {obj.name} error {e}")

    def set_parent(self):
        for layer in self.layers:
            for obj in layer:
                obj.set_parent()

    def render(self, surface: pygame.Surface):
        """등록된 객체에 render 함수를 실행합니다

        Args:
            surface (pygame.Surface): 화면 스크린
        """
        for layer in self.layers:
            for obj in layer:
                if obj.location.world_visible:
                    for component in obj.components:
                        #try:
                        component.render(surface, self.camera)
                        #except Exception as e:
                        #    print(f"RENDER {obj.name} components name: {component.__class__} error {e}")
                    #try:
                    obj.render(surface, self.camera)
                    #except Exception as e:
                    #    print(f"RENDER {obj.name} error {e}")


    
    def add(self, obj: 'GameObject'):
        """
        오브젝트를 추가함
        
        Args:
            obj (GameObject): GameObject 를 상속받은 클래스
        
        """
        layer = self.layers[obj.layer]
        layer.append(obj)
    
    def absorb(self, list : Sequence['GameObject']):
        """
        오브젝트 집합을 추가함
        
        Args:
            list (list): 오브젝트 리스트
        
        """
        for obj in list:
            self.add(obj)
    
    def remove(self, obj: 'GameObject'):
        """오브젝트를 새계에서 삭제하지만 오브젝트 자체는 삭제되지않음"""
        self.layers[obj.layer].remove(obj)
            
    def clear(self):
        """모든 오브젝트를 새계에서 삭제하고 오브젝트 객체도 삭제됨 (delete 함수 실행)
        """
        for layer in self.layers:
            for _ in range(len(layer)):
                layer[0].delete()
    
    def get_object(self, obj_name) -> 'GameObject':
        if obj_name in self.obj_cache:
            return self.obj_cache[obj_name]

        for layer in self.layers:
            for i in range(len(layer)):
                if layer[i].name == obj_name:
                    self.obj_cache[obj_name] = layer[i]
                    return layer[i]
 
    @property
    def display(self):
        return self.__display
    
    @display.setter
    def display(self, value):
        self.__display = value
        self.camera = self.get_object(value)

    def load(self, path: str):
        """오브젝트를 생성하고 새계에 등록합니다

        Args:
            path (str): 멥 파일에 경로 .json

        Raises:
            ImportError: path 경로에 json 에서 class_list 에 존재하지 않는 클래스를 불러오려 할때
            ValueError: 매개변수와 json 에서 저장된 값에 이름이 다르면
        """
        json : dict = _util.replaced_jgetter(_util.jsopen(path))
        setting : dict =json['setting']
        objs =  json['objs']

        # 로딩 길이 계산 (타일, 서피스, 스프라이트 시트, 게임오브젝트 포함)
        tile_len = sum([len(i[2]) for i in setting.get('tile', [])])
        surface_len = sum([len(i[2]) for i in setting.get('surface', [])])
        sprite_sheet_len = sum([i[4] for i in setting.get('sprite_sheet', [])])  # 스프라이트 시트의 총 타일 수

        gameobject_len = sum([len(j) for i in objs for j in list(i.values())])

        loading_length = tile_len + surface_len + sprite_sheet_len + gameobject_len

        loading_cnt = 0

        def draw(): #로딩바. 붉은 표면 준비가 느려져서 플래이어를 위한 표시시
            rect = pygame.Rect(10, 10, loading_cnt/loading_length*(Manger.WIDTH-20), 20)
            pygame.draw.rect(Manger.screen, (255, 255, 255), rect)
            pygame.display.update(rect)

        # 타일 시트 로드
        tile_sheet = {}
        for tile_value in setting.get('tile', []):
            tile_sheet[tile_value[0]] = TileSheet(*tile_value)
            loading_cnt += len(tile_value[2])
            draw()

        Manger.tile_sheet = tile_sheet

        # 서피스 시트 로드
        surface_sheet = {}
        for surface_value in setting.get('surface', []):
            surface_sheet[surface_value[0]] = SurfaceSheet(*surface_value) 
            loading_cnt += len(surface_value[2])
            draw()

        Manger.surface_sheet = surface_sheet

        # 스프라이트 시트 로드
        sprite_sheet = {}
        for sprite_value in setting.get('sprite_sheet', []):
            sprite_sheet[sprite_value[0]] = SpriteSheet(*sprite_value)
            loading_cnt += sprite_value[4]  # 총 타일 수만큼 증가
            draw()
        
        Manger.sprite_sheet = sprite_sheet
        
        setting.pop("tile")
        setting.pop("surface")
        setting.pop("sprite_sheet")
        
        for key, value in setting.items():
            setattr(Manger, key, value)

        parent_object = ParentObject()
        parent_object.init_instantiate()

        for map_objs in objs:
            for name in map_objs.keys():
                for json_object in map_objs[name]:
                    draw()
                    loading_cnt += 1
                    try:
                        args = list(json_object.values())
                        parameters = list(json_object.keys())
                        prefab_class: 'GameObject' = Manger.classes.get(name, None) # 우선적으로 같은 이름에 게임 오브젝트 클래스를 가져옴옴
                        if prefab_class == None:
                            prefab_class = globals().get(name, None) # pygamefwk 라이브러리 내부에 게임 오브젝트를 가져오는거임임
                            if prefab_class == None:
                                raise ImportError(f"{name} 클레스가 존재하지 않거나 불러지지 않았습니다. \n 현재 불러온 클래스 {Manger.classes}")

                        cls_parameters = list(inspect.signature(prefab_class).parameters.keys())

                        if cls_parameters[-1] == "kwargs":
                            cls_parameters.pop()

                        if cls_parameters == parameters: # 클래스에서 요구하는 파라미터랑 json에서 작성된 값이 같아야 한다. (변수명)
                            prefab: 'GameObject' = prefab_class(*args)
                            if args[0] == "main_cam":
                                self.camera = prefab
                            prefab.init_instantiate()
                            prefab.child_instantiate()
                        else:
                            raise ValueError(f"이름이 틀리거나 순서가 다른것같습니다.\njson :{parameters}\n{name} class:{cls_parameters}")
                    except ValueError as e:
                        print("Value Error message: ", e)
                    except ImportError as e:
                        print("Import Error message: ", e)

        self.set_parent()

        parent_object.location.set_world() # 각 오브젝트 world_position 생성