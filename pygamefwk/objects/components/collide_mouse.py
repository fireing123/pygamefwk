from typing import List, TYPE_CHECKING
from pygamefwk.objects.components.reset import on_reset

if TYPE_CHECKING:
    from pygamefwk.objects.components.image import ImageObject

collide_images: List[List['ImageObject']] = [[],[],[],[],[],[],[],[],[],[]]

def reset():
    for layer in collide_images:
        layer.clear()

on_reset.add_lisner(reset)