from pygamefwk.objects.ui.ui import UI
from pygamefwk.event import Event
from pygamefwk.input import Input
from pygamefwk.objects.components.image import ImageObject

class Button(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, default, **kwargs):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        if default != None:
            kwargs["path"] = default
        self.image = ImageObject(self, follow=True, collide=True, **kwargs)
        self.components.append(self.image)

        self.dark = ImageObject(self, surface=self.image.og_image.get_size(), follow=True)
        self.components.append(self.dark)
        
        self.dark.og_image.fill((0,0,0,20))
        self.dark.visible = False

        self.rect = self.image.rect
        self.is_click = Event()
    
    def on_mouse_stay(self, pos):
        if Input.get_mouse_down(0):
            self.dark.visible = True
        elif Input.get_mouse_up(0):
            if self.dark.visible:
                self.is_click.invoke()
            self.dark.visible = False
    
    def on_mouse_exit(self, pos: tuple[int, int]):
        self.dark.visible = False