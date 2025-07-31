
# 편의성 import

__version__ = "1.0.1"

from pygamefwk.objects.component import Component

from pygamefwk.manger    import Manger
from pygamefwk           import game
from pygamefwk.game      import Game
from pygamefwk.objects   import *
from pygamefwk.sheet     import SurfaceSheet, TileSheet
from pygamefwk.timertask import TimerTask, OnceTimerTask
from pygamefwk.input     import Input
from pygamefwk.event     import Event
from pygamefwk.location  import Location
from pygame.math import Vector2 as Vector

from pygame import (
    Surface,
    Rect
)

from pygame.constants import *
