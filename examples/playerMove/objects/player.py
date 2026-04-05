from pygamefwk import *

class Player(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        img = ImageObject(self, surface=[30, 30])
        img.og_image.fill((255, 255, 255))
        self.components.append(img)


    def update(self):
        vec = Vector(0, 0)
        if Input.get_key(K_a):
            vec.x -= 1
        if Input.get_key(K_s):
            vec.y -= 1
        if Input.get_key(K_w):
            vec.y += 1
        if Input.get_key(K_d):
            vec.x += 1

        if vec != Vector(0, 0):
            vec = vec.normalize()
        
        self.location.translate(vec * 10)

        