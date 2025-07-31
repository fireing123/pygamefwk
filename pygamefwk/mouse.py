"""
pygame 의 마우스르 상속받음
"""
from pygamefwk.manger import Manger
from pygamefwk.objects.components.collide_mouse import collide_images
from pygame.mouse import *
from pygamefwk import Vector

def inget_pos():
    pos = Vector(get_pos())
    pos.x -= Manger.WIDTH / 2
    pos.y += Manger.HEIGHT / 2
    return pos

def mouse_event():
    """이미지 오브젝트의 마우스 충돌연산
    """
    for layer in collide_images[::-1]:
        for img_obj in layer[::-1]:
            if img_obj.rect != None and img_obj.object.location.world_visible:
                if img_obj.rect.collidepoint(get_pos()):
                    if img_obj.collide_state == False:
                        img_obj.collide_state = True
                        img_obj.object.on_mouse_enter(get_pos())
                        return 
                    elif img_obj.collide_state == True:
                        img_obj.object.on_mouse_stay(get_pos())
                        return 
                elif img_obj.collide_state == True:
                    img_obj.collide_state = False
                    img_obj.object.on_mouse_exit(get_pos())
                    return 
