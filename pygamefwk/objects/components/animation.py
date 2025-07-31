from pygamefwk.objects.component import Component
from pygamefwk.timertask import TimerTask
from pygamefwk.manger import Manger
from pygamefwk.event import Event

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygamefwk.objects.components.image import ImageObject

class Animation(Component):
    """주기적으로 이미지를 변경함"""
    def __init__(self, tick, image_object: 'ImageObject', **kwargs):
        self.object = image_object
        self.period = TimerTask(tick)
        self.index = 0
        self.on_end = Event()
        if 'sheet' in kwargs:
            self.sheet = Manger.surface_sheet[kwargs['sheet']]
            if 'range' in kwargs:
                frist, last = kwargs['range']
                self.images = self.sheet.images[frist:last]
            else:
                self.images = self.sheet.images
        else:
            raise ValueError("키워드가 적절하지 않습니다. sheet 키워드에 사용하는 시트에 이름을 작성하세요")
        self.event_invoked = False
        self.once = kwargs.get('once', False)
        self.len = len(self.images)
        
    def reset(self):
        self.event_invoked = False
        self.period.reset()
        self.pointToIndex(0)

    def pointToIndex(self, index):
        self.index = index
        self.change_image()

    def update(self):
        if self.period.run_periodic_task():
            self.change_image()

    def change_image(self):
        self.object.set_orginal_image(self.images[self.index])
        self.index += 1
        if self.index == self.len:
            if self.once:
                if not self.event_invoked:
                    self.on_end.invoke()
                    self.event_invoked = True
                self.index = self.len -1
            else:
                self.on_end.invoke()
                self.index = 0