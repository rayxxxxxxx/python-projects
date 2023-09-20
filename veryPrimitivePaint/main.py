import sys

import pygame as pg

from primitive_paint import PrimitivePaint

def main():
    clock = pg.time.Clock()
    screen = pg.display.set_mode((800, 800))

    pp = PrimitivePaint((800, 800), (0, 0))
    pp.PAINT_SIZE = 20

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if pg.mouse.get_pressed()[0]:
                pp.draw(pg.mouse.get_pos(), (255, 255, 255))
            elif pg.mouse.get_pressed()[2]:
                pp.draw(pg.mouse.get_pos(), (0, 0, 0))

            if pg.key.get_pressed()[pg.K_c]:
                pp.clear()

        pp.render(screen)
        
        pg.draw.circle(screen, 'white', pg.mouse.get_pos(), pp.PAINT_SIZE, 1)

        clock.tick(60)
        pg.display.update()


if __name__ == '__main__':
    main()
