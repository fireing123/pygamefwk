from pygamefwk.objects.component import Component
from pygamefwk.objects.components.reset import on_reset

def reset():
    SoundListener.listener = None

on_reset.add_lisner(reset)

class SoundListener(Component):
    """소리를 듣는 위치"""
    listener = None

    def __init__(self, object) -> None:
        self.object = object
        if SoundListener.listener != None:
            raise ValueError("이미 SoundListener 컴포넌트는 존재합니다")
        SoundListener.listener = self