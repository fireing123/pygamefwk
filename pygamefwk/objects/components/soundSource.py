import pygame
from pygamefwk.objects.component import Component
from pygamefwk.objects.components.soundListener import SoundListener

class SoundSource(Component):
    """소리를 재생, 정지하며
    거리에따른 음량조절을 할수있다."""
    def __init__(self, object, path, volume, vol_lambda, mode=None):
        self.vol_lambda = vol_lambda
        self.object = object
        self.volume = volume
        match mode:
            case None:
                self.mode = "sound"
                self.sound = pygame.mixer.Sound(path)
            case "endPlay":
                self.mode = "end"
                self.sound = path

    def set_volume(self):
        distance = self.object.location.world_position.distance_to(SoundListener.listener.object.location.world_position if SoundListener.listener != None else (0, 0))
        volume = self.vol_lambda(distance)

        if self.mode == "sound":
            self.sound.set_volume(volume + self.volume)
            
        elif self.mode == "end":
            pygame.mixer.music.set_volume(volume + self.volume)

    def play(self, loops=0, maxtime=0, fade_ms=0, start=0):
        distance = self.object.location.world_position.distance_to(SoundListener.listener.object.location.world_position if SoundListener.listener != None else (0, 0))
        volume = self.vol_lambda(distance)

        if self.mode == "sound":
            self.sound.set_volume(volume + self.volume)
            self.sound.play(loops, maxtime, fade_ms)
            
        elif self.mode == "end":
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.sound)
            pygame.mixer.music.set_volume(volume + self.volume)
            pygame.mixer.music.play(loops, start, fade_ms)
            
    def stop(self):
        if self.mode == "sound":
            self.sound.stop()
        elif self.mode == "end":
            pygame.mixer.music.stop()

class SoundManager(Component):
    def __init__(self, dict):
        self.dict = dict

    def play(self, name, loops=0):
        try:
            self.dict[name].play(loops=loops)
        except Exception as e:
            print(e, " 이름이 틀릴 가능성이 높음")

    def stop(self, name):
        try:
            self.dict[name].stop()
        except Exception as e:
            print(e, " 이름이 틀릴 가능성이 높음")

    def mixer_stop(self):
        pygame.mixer.music.stop()