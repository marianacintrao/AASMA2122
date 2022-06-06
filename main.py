import string
import sys
import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import Fish


SCALE_FACTOR = 1
width, height = (1000, 500)
fps = 60.0

def draw(screen, particles, color, radius):
    for p in particles:
        pg.draw.circle(screen, color, p, radius)
    # pg.display.flip()
    pg.display.update()

# def render_text(screen, what, color, where):
#     font = pg.font.SysFont('monospace', 20)
#     text = font.render(str(what), 1, pg.Color(color))
#     screen.blit(text, where)


def requestInput(name: string, default: int):
    
    while True:
        inp = input("Enter number of %s, default is %d: " % (name, default))
        if not inp.strip():
            return default
            
        if not inp.isnumeric() or int(inp) <= 0:
            print("Please enter an integer larger than 0")
            continue
        else:
            return int(inp)


def setupScreen():
    pg.init()
    pg.display.set_caption('')

    # Set up the window.
    screen = pg.display.set_mode((width, height))
    fpsClock = pg.time.Clock()
    screen.fill((255, 255, 255))

    positions = np.random.rand(n_fishes, 2).dot( \
                np.array([[width, 0], \
                          [0, height]]) )

    # velocities = (np.random.rand(n_fishes, 2) * 2) - 1

    # text_toggles = True
    # dt = 1/fps
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit() 
                sys.exit()

        # # Clear screen
        screen.fill((255, 255, 255))

        draw(screen, positions*SCALE_FACTOR, (100, 100, 200), 5)

        dt = fpsClock.tick(fps)


if __name__ == '__main__':
    print("Hello, welcome to our aquarium simulator!")
    
    n_fishes = requestInput(name="fishes", default=20)
    n_sharks = requestInput(name="sharks", default=1)
    n_plankton = requestInput(name="plankton", default=20)

    print("\n===============================")  
    print("Fish initial population: " + str(n_fishes))
    print("Shark initial population: " + str(n_sharks))
    print("Plankton initial population: " + str(n_plankton))
    print("===============================\n")

    # fishList = [Fish() for i in range(n_fishes)]


    #Set up screen
    setupScreen()

    
