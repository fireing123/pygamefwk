from pygamefwk.objects.component import Component
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from pygamefwk.objects.gameobject import GameObject
    from pygamefwk.objects.components.animation import Animation

class AnimationManager(Component):
    def __init__(self, object: 'GameObject', animations: Dict[str, 'Animation'], start_key: str):
        self.object = object
        self.animations = animations
        self.state = start_key
    
    def change_animation(self, animation_name, reset=False):
        if self.state != animation_name:
            self.state = animation_name
            self.animations[self.state].reset()
        else:
            if reset:
                self.animations[self.state].reset()

    def update(self):
        self.animations[self.state].update()