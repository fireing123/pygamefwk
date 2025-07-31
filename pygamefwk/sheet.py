"""이미지를 시작 단계에서 미리 불러옴"""
from pygame import image, PixelArray, Surface
from pygame.transform import scale
from pygamefwk.objects.components.image import red

class SurfaceSheet:
    def __init__(self, name, is_hits, paths, default):
        self.name = name
        self.size = default
        cache = [image.load(path).convert_alpha() if path != None else None for path in paths]
        self.images = []
        for surf in cache:
            if surf == None: 
                self.images.append(None)
                continue

            xs, ys = surf.get_size()
            img = scale(surf, (xs*default, ys*default))
            if is_hits:
                red[img] = scale(get_hit_image(surf), (xs*default, ys*default))
            self.images.append(img)
    
class TileSheet:
    def __init__(self, name, is_hits, paths, default):
        self.name = name
        self.size = default
        cache = [image.load(path).convert_alpha() if path != None else None for path in paths]
        self.surfaces = []

        for mage in cache:
            if mage == None: 
                self.surfaces.append(None)
                continue

            img = scale(mage, (default, default))
            if is_hits:
                red[img] = scale(get_hit_image(mage), (default, default))
            self.surfaces.append(img)


def get_hit_image(s: Surface): # 매우 느립니다. 그래서 초기 시작부분에 미리 사용합니다.
    """이미지에 대해 상대적으로 빨갛게 물들입니다."""
    f = s.copy()
    f.lock()
    p = PixelArray(f)
    h=f.get_height()
    j=f.unmap_rgb
    for w in range(f.get_width()):
        l=p[w]
        for y in range(h):
            t = j(l[y])
            r = t.r + 100
            o = (r % 255) // 2
            t.r = r if r<255 else 255
            t.g = max(t.g-o,0)
            t.b = max(t.b-o,0)
            l[y] = t
    del p
    f.unlock()
    return f