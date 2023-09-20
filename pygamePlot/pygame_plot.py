from abc import ABC
from typing import Tuple

import numpy as np
import pygame as pg


ORIGIN_SCALERS = {
    'm': (0.5, 0.5),
    'l': (0, 0.5),
    'c': (0, 1)
}


def calculate_origin_point(width: float, height: float, origin: str) -> tuple:
    x_origin = width*ORIGIN_SCALERS[origin][0]
    y_origin = height*ORIGIN_SCALERS[origin][1]
    return (x_origin, y_origin)


def check_data(x: list | np.ndarray, y: list | np.ndarray):
    if isinstance(x, list) and isinstance(y, list):
        if len(x) == 0 or len(y) == 0:
            raise Exception("zero size data")
    elif isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        if x.size == 0 or y.size == 0:
            raise Exception("zero size data")
    else:
        raise Exception("invalid data types")


class Axes(ABC):
    _srf: pg.Surface = None
    _srf_width: int = None
    _srf_height: int = None
    _srf_center: tuple[float] = None

    _xlim: tuple[float] = None
    _ylim: tuple[float] = None
    _center: tuple[float] = None

    _origin: str = 'm'

    def __init__(self, size: tuple, xlim: tuple, ylim: tuple, origin: str = 'm') -> None:
        super().__init__()
        self._srf = pg.Surface(size)
        self._srf_width = size[0]
        self._srf_height = size[1]
        self._srf_center = calculate_origin_point(size[0], size[1], origin)
        self._xlim = xlim
        self._ylim = ylim
        self._center = ((xlim[0]+xlim[1])/2, (ylim[0]+ylim[1])/2)
        self._origin = origin

    @property
    def surface(self) -> pg.surface.Surface:
        return self._srf

    @property
    def width(self) -> int:
        return self._srf_width

    @property
    def height(self) -> int:
        return self._srf_height

    @property
    def size(self) -> Tuple:
        return (self._srf_width, self._srf_height)

    @property
    def srf_center(self) -> Tuple:
        return self._srf_center


class PygamePlot(Axes):
    def __init__(self, size: tuple, xlim: tuple, ylim: tuple, origin: str = 'm') -> None:
        super().__init__(size, xlim, ylim, origin)
        self.show_axis_line: bool = True
        self.face_color: tuple = (0, 0, 0)
        self.axis_line_color: tuple = (128, 128, 128)

    def _translate(self, p: tuple | list | np.ndarray) -> Tuple:
        x = p[0]/(self._xlim[1]-self._xlim[0]) * \
            self._srf_width+self._srf_center[0]
        y = -p[1]/(self._ylim[1]-self._ylim[0]) * \
            self._srf_height+self._srf_center[1]

        return (x, y)

    def _draw_axis(self) -> None:
        pg.draw.line(self._srf,
                     self.axis_line_color,
                     (0, self.srf_center[1]),
                     (self._srf_width, self.srf_center[1]))
        pg.draw.line(self._srf,
                     self.axis_line_color,
                     (self.srf_center[0], 0),
                     (self.srf_center[0], self._srf_height))

    def plot(self, x: list | np.ndarray, y: list | np.ndarray, c: tuple = (255, 255, 255), lw: int = 1) -> None:
        check_data(x, y)
        for i in range(len(x) - 1):
            pg.draw.line(
                self._srf,
                c,
                self._translate(np.array([x[i], y[i]])),
                self._translate(np.array([x[i + 1], y[i + 1]])),
                lw
            )

    def scatter(self, x: np.ndarray, y: np.ndarray, c: tuple = (0, 255, 128), ps: int = 1, pw: int = 0) -> None:
        check_data(x, y)
        for i in range(len(x)):
            pg.draw.circle(
                self._srf,
                c,
                self._translate(np.array([x[i], y[i]])),
                ps,
                pw
            )

    def point(self, x: int | float, y: int | float, c: tuple = (255, 255, 255), ps: int = 1, pw: int = 0):
        pg.draw.circle(
            self._srf,
            c,
            self._translate(np.array([x, y])),
            ps,
            pw
        )

    def hline(self, y: float, c: tuple = (255, 255, 255), lw: int = 1):
        pg.draw.line(
            self._srf,
            c,
            self._translate(np.array([-self._srf_width, y])),
            self._translate(np.array([self._srf_width, y])),
            lw
        )

    def vline(self, x: float, c: tuple = (255, 255, 255), lw: int = 1):
        pg.draw.line(
            self._srf,
            c,
            self._translate(np.array([x, -self._srf_height])),
            self._translate(np.array([x, self.height])),
            lw
        )

    def render(self, srf: pg.Surface, dest: tuple = (0, 0)) -> None:
        if self.show_axis_line:
            self._draw_axis()
        srf.blit(self._srf, dest)
        self._srf.fill(self.face_color)
