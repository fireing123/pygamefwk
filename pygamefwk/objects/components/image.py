import pygame
from pygamefwk.objects.component import Component
from pygamefwk.objects.gameobject import GameObject
from pygamefwk.manger import Manger
from pygame.math import Vector2 as Vector
from pygamefwk.objects.components.collide_mouse import collide_images
from pygamefwk.objects.components.reset import on_reset

red = {}

def reset():
    red.clear()

on_reset.add_lisner(reset)

cache = {}

class ImageObject(Component):
    """오브젝트에 위치, 각도를 기준으로 이미지를 렌더링함"""
    def __init__(self, object: GameObject, **kwargs):
        self.object: GameObject = object
        self.visible = True
        self.og_image = None
        self.low_mode = None

        if 'low_mode' in kwargs:
            self.low_mode = kwargs['low_mode'] # name, xy, left args
            self.og_image = pygame.Surface((self.low_mode[1]), pygame.SRCALPHA).convert_alpha()
            getattr(pygame.draw, self.low_mode[0])(self.og_image, *self.low_mode[2:])


        if 'path' in kwargs:
            if kwargs['path'] not in cache:
                cache[kwargs['path']] = pygame.image.load(kwargs['path']).convert_alpha()

            self.og_image = cache[kwargs['path']]

        if 'surface' in kwargs:
            self.og_image = pygame.Surface(kwargs['surface'], pygame.SRCALPHA).convert_alpha()
        elif 'value' in kwargs:
            self.og_image = kwargs['value']

        if 'size' in kwargs:
            size = Vector(self.og_image.get_size())
            sizeup = Vector(kwargs['size'])
            size.x *= sizeup.x
            size.y *= sizeup.y
            self.og_image = pygame.transform.scale(self.og_image, size)

        self.collide = kwargs.get("collide", False)
        if self.collide:
            self.collide_state = False
            collide_images[object.layer].append(self)
        self.camera_staticable = kwargs.get("follow", False)
        self.flip = kwargs.get("filp", [False, False]) # 반전하면 True
        self.type = 'center' if kwargs.get('type') == None else kwargs['type']
        
        # 사이즈 벡터 변수 추가 (뽀잉뽀잉 효과용)
        self.size_vector = Vector(1.0, 1.0)  # 기본 크기 1배

        self.image = self.og_image

        if self.og_image != None:
            self.rect = self.image.get_rect()
        self.camera = Manger.scene.camera
        self.__cellophane = False

    def set_flip(self, value):
        if not (self.flip[0] == value):
            self.flip[0] = value

    def set_cellophane(self, value):
        if self.__cellophane != value:
            self.__cellophane = value

    def set_orginal_image(self, image):
        self.og_image = image

    def set_size_vector(self, size_vector: Vector):
        """사이즈 벡터 설정 (뽀잉뽀잉 효과용)"""
        self.size_vector = size_vector

    def get_size_vector(self) -> Vector:
        """현재 사이즈 벡터 반환"""
        return self.size_vector

    def delete(self):
        try:
            if self.collide:
                collide_images[self.object.layer].remove(self)
        except: pass

    def render(self, surface, camera):
        if self.visible and self.og_image != None:
                
            image = red[self.og_image] if self.__cellophane else self.og_image # 만약 칠하면 og_image 주소를 키로 접근해 칠해진 image 를 얻음

            if self.camera_staticable: # 돌린 직사각형의 위치를 설정합니다
                rotated_rect = get_rotated_range(image.get_rect(), self.object.location.world_rotation)
                setattr(rotated_rect, self.type, camera.centerXY(self.object.render_position))
            else:
                rotated_rect = get_rotated_range(image.get_rect(), self.object.location.world_rotation + camera.location.world_rotation)
                setattr(rotated_rect, self.type, camera(self.object.render_position))

            if rotated_rect.colliderect(0, 0, Manger.WIDTH, Manger.HEIGHT): # 화면안에 일부라도 있으면 실행합니다
                # 사이즈 벡터 적용 (rotate 전에 적용)
                if self.size_vector != Vector(1.0, 1.0):
                    original_size = image.get_size()
                    new_size = (int(original_size[0] * self.size_vector.x), int(original_size[1] * self.size_vector.y))
                    image = pygame.transform.scale(image, new_size)
                
                self.image = pygame.transform.flip(image, *self.flip)
                if self.camera_staticable: # 이미지를 실제도 돌립니다
                    self.image = pygame.transform.rotate(self.image, self.object.location.world_rotation)
                else:
                    self.image = pygame.transform.rotate(self.image, self.object.location.world_rotation + camera.location.world_rotation)

                if self.camera_staticable: # 이미지의 위치를 지정합니다
                    self.rect = self.image.get_rect(**{self.type:camera.centerXY(self.object.render_position)})
                else:
                    self.rect = self.image.get_rect(**{self.type:camera(self.object.render_position)})
                surface.blit(self.image, self.rect)

def get_rotated_range(rect: pygame.Rect, angle):
    """angle 각도로 돌린 직사각형과 외접하는 큰 직사각형을 반환합니다!"""
    if angle == 0:
        return rect
    
    cx, cy = rect.center

    corners = [
        rect.topleft,
        rect.topright,
        rect.bottomright,
        rect.bottomleft
    ]

    rotated_corners = [rotate_vector(x, y, cx, cy, angle) for (x, y) in corners]

    min_x = min(x for (x, y) in rotated_corners)
    max_x = max(x for (x, y) in rotated_corners)
    min_y = min(y for (x, y) in rotated_corners)
    max_y = max(y for (x, y) in rotated_corners)

    rotated_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    return rotated_rect

def rotate_vector(x, y, rx, ry, angle):
    nvector = Vector(x - rx, y - ry).rotate(angle)
    return nvector