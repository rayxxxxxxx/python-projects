import sys
import math

import numpy as np
import pygame as pg

from pygame_plot import PygamePlot


def main():

    w = 800
    h = 600

    xmin, xmax = -10, 10
    ymin, ymax = -2, 2

    x1 = np.linspace(xmin, xmax, 20)
    x2 = np.linspace(xmin, xmax, 200)

    pg_plot = PygamePlot((w, h), (xmin, xmax), (ymin, ymax),  'm')

    t = 0
    dt = 0.05
    clock = pg.time.Clock()
    screen = pg.display.set_mode((w, h))
    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()

        pg.display.set_caption(str(int(clock.get_fps())))

        y1 = np.sin(0.25*x1-t)
        y2 = np.exp(-0.1*x2**2)*np.cos(2*x2-t)

        pg_plot.hline(1.0, (255, 0, 0), 2)
        pg_plot.vline(1.0, (0, 255, 0), 2)

        pg_plot.scatter(x1, y1, c=(255, 255, 255), ps=2, pw=0)

        pg_plot.plot(x2, y2, c=(255, 255, 255), lw=1)

        pg_plot.render(screen, dest=(0, 0))

        t = (t+dt) % (2*math.pi)

        clock.tick(60)
        pg.display.update()


if __name__ == '__main__':
    main()
