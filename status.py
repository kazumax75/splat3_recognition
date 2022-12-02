
from enum import IntEnum

class GAME(IntEnum):
    NONE = 0
    READY = 1
    PLAYING = 2
    MAP = 3

class Status(IntEnum):
    NONE = 0
    ALIVE = 1
    DEATH = 2
    SP = 3
    HAS_HOKO = 4
    
class TEAM(IntEnum):
    ALLY = 0
    ENEMY = 1