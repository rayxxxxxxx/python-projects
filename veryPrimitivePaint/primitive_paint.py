
from typing import Tuple

import numpy as np
import pygame as pg


class PrimitivePaint:

    def __init__(self, size: tuple, dest: tuple) -> None:
        self._size = size
        self._srf = pg.Surface(size)
        self._dest = dest
        self.PAINT_SIZE: int = 10
        self.BG_COLOR: Tuple = (0, 0, 0)
        self._srf.fill(self.BG_COLOR)

    @property
    def surface(self):
        return self._srf

    @property
    def size(self):
        return self._size

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    def draw(self, mpos: Tuple, color: Tuple = (255, 255, 255)):
        pg.draw.circle(self.surface,
                       color,
                       np.array(mpos) - np.array(self._dest),
                       self.PAINT_SIZE)

    def render(self, srf: pg.Surface):
        srf.blit(self._srf, self._dest)

    def clear(self):
        self._srf.fill(self.BG_COLOR)
