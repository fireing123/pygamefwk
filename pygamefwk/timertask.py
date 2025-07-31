import inspect
from pygame import time
from typing import Callable
from pygamefwk.error import FunctionError

class TimerTask:
    """여러번 체크합니다"""
    def __init__(self, tick: int, event: Callable = lambda:None, *value, **kwargs):
        self.tick = tick
        self.last_update = 0
        if inspect.ismethod(event) and inspect.isfunction(event):
            raise FunctionError(f"입력받은 값은 는 함수가 아닙니다")
        self.event = event
        self.value = value
        self.kwargs = kwargs
        
    def not_update_run(self):
        """시간이 지났나 검사하기만 합니다"""
        if time.get_ticks() - self.last_update > self.tick:
            self.event(*self.value, **self.kwargs)
            return True
        return False

    def run_periodic_task(self):
        """시간이 지났나 검사, 리셋합니다"""
        if time.get_ticks() - self.last_update > self.tick:
            self.reset()
            self.event(*self.value, **self.kwargs)
            return True
        return False
    
    def reset(self):
        self.last_update = time.get_ticks()
        
class OnceTimerTask(TimerTask):
    """한번 체크하면 리셋할떄까지 체크를 하지 않습니다."""
    def __init__(self, tick, event=lambda:None, *value, **kwargs):
        super().__init__(tick, event, *value, **kwargs)
        self.once = False
    
    def run_periodic_task(self):
        if time.get_ticks() - self.last_update > self.tick and not self.once:
            self.event(*self.value, **self.kwargs)
            self.once = True
            return True
        return False
    
    def reset(self):
        super().reset()
        self.once = False
    