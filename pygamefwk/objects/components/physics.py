from pygame import Rect

from pygamefwk.objects                   import Component, GameObject
from pygamefwk.objects.components.reset  import on_reset
from pygamefwk.event                     import Event
from pygamefwk.vector                    import Vector

from collections import deque
from typing import List

physics_grounds: List[Rect] = []
physics_objects: List['Physics'] = []

def reset():
    physics_grounds.clear()
    physics_objects.clear()

on_reset.add_lisner(reset)

gravity = 0.5

class Physics(Component):
    def __init__(self, object: GameObject, rect: Rect, **kwargs) -> None:
        self.object = object
        self.rect = rect
        self.on_ground = False
        self.friction = 0.45
        self.air_friction = 0.1
        self.velocity = Vector(0, 0)
        self.type: str = kwargs.get('type', 'center')
        physics_objects.append(self)
        self.collision_enter_event = Event()

    def delete(self):
        try:
            physics_objects.remove(self)
        except: pass

    def add_force(self, velocity: Vector):
        self.velocity += velocity

    def step(self):
        self.on_ground = False    
        next_rect = self.rect.copy()
        setattr(next_rect, self.type, self.object.location.position + self.velocity)
        queue = deque()
        for ground in physics_grounds:
            if ground.colliderect(next_rect):
                collide_type = None
                if next_rect.top > ground.bottom - 21:
                    next_rect.top = ground.bottom - 1
                    self.velocity.y = max(self.velocity.y, 0)
                    collide_type = 0 # ground
                    self.on_ground = True
                else:
                    if next_rect.bottom < ground.top + 20:
                        next_rect.bottom = ground.top - 1
                        self.velocity.y = min(self.velocity.y, 0)
                        collide_type = 1 # top
                    elif next_rect.left > ground.right - 15:
                        next_rect.left = ground.right
                        self.velocity.x = min(self.velocity.x, 0)
                        collide_type = 2 # left
                    elif next_rect.right < ground.left + 15:
                        next_rect.right = ground.left
                        self.velocity.x = max(self.velocity.x, 0)
                        collide_type = 3 # right
                queue.append((ground, collide_type))

        while queue:
            ground, collide_type = queue.popleft()
            self.collision_enter_event.invoke(ground, collide_type)

        self.rect = next_rect
        self.object.location.position = getattr(next_rect, self.type)

        self.velocity.y -= gravity

        if self.velocity.y < -20: # 종속 속도
            self.velocity.y += gravity + self.air_friction
        
        if self.velocity.x < -0.2:
            if self.on_ground:
                self.velocity.x += self.friction
            else:
                self.velocity.x += self.air_friction
        elif self.velocity.x > 0.2:
            if self.on_ground:
                self.velocity.x -= self.friction
            else:
                self.velocity.x -= self.air_friction
        else:
            self.velocity.x = 0