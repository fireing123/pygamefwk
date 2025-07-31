import pygame
from pygamefwk.objects.ui import NEWLINE
from pygamefwk.objects.ui.ui import UI
from pygamefwk.vector import Vector

# (path, size): font
class Text(UI):
    """글자를 화면에 나타냄"""
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, size, color, Font, interval, **kwargs):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.Font = Font

        if Font.startswith('./'):
            self.font = pygame.font.Font(Font, size)
        else: 
            self.font = pygame.font.SysFont(Font, size)

        if 'bold' in kwargs:
            self.font.set_bold(kwargs['bold'])

        self.render_type = kwargs.get("render_type", "topleft")

        self.__shadow = kwargs.get("shadow", None)
        self.shadow_pos = [1, 1]

        self.size = size
        self.interval = interval
        self.__color = color
        self.__text = ""
        self.changed = True
        self.render_standard = None
        self.images = None
    
    @property
    def text(self):
        return self.__text
    
    @text.setter
    def text(self, value):
        self.__text = value
        self.changed = True

    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, color):
        self.__color = color
        self.changed = True

    @property
    def shadow(self):
        return self.__shadow
    
    @shadow.setter
    def shadow(self, color):
        self.__shadow = color
        self.changed = True

    def set_position_standard(self, standard):
        self.render_standard = standard

    def get_position(self, index: int) -> Vector:
        """글자에 index 주소로 접근해서 Text 오브젝트 위치를 기준으로 글자에 상대적 위치를 반환

        Args:
            __index (int): 글자 위치

        Returns:
            Vector: position 을 0, 0 으로 할때 x,y 좌표
        """
        line = self.get_line(index)
        text = self.text[:index].split(NEWLINE)[-1]
        x, _ = self.font.size(text)
        y = self.size + self.interval
        y *= line
        return Vector(x-5, -y)

    def get_line(self, index: int) -> int:
        """글자에 index 주소로 접근해서 줄수를 확인함

        Args:
            __index (int): 글자위치

        Returns:
            int: 라인 번호
        """
        line = self.text.count(NEWLINE, 0, index)
        return line + 1

    def render(self, surface : pygame.Surface, camera):
        if self.changed:
            texts = self.text.split(NEWLINE)
            self.images = [self.font.render(text, True, self.__color) for text in texts]
            if self.__shadow != None:
                self.shadow_images = [self.font.render(text, True, self.__shadow) for text in texts]
            if len(self.__color) == 4:
                for image in self.images:
                    image.set_alpha(self.__color[3])
            
            if self.__shadow != None:
                if len(self.__shadow) == 4:
                    for shadow_image in self.shadow_images:
                        shadow_image.set_alpha(self.__shadow[3])
            self.changed = False

        position = self.location.world_position if self.render_standard == 'mouse' else self.render_position
        if self.__shadow != None:
            pos = camera.centerXY(position)
            pos.x += self.shadow_pos[0]
            pos.y += self.shadow_pos[1]
            for image in self.shadow_images:
                rect = image.get_rect()
                setattr(rect, self.render_type, pos)
                pos.y += self.size + self.interval
                surface.blit(image, rect)

        pos = camera.centerXY(position)
        for image in self.images:
            rect = image.get_rect()
            setattr(rect, self.render_type, pos)
            pos.y += self.size + self.interval
            surface.blit(image, rect)
