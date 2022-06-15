from msilib.schema import Environment
from resources.consts import map_size
import string
import sys
import numpy as np
import os
import pygame as pg
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


from Environment import Environment
import resources.consts as consts
#from resources.consts import width, height 

params = {
    'speed': 0.004,
    'influence_prox': consts.influence_prox,
    'alignment_factor': 0.005,
    'cohesion_factor': 0.005,
    'separation_factor': 0.0002
}

SCALE_FACTOR = 50

width = SCALE_FACTOR * map_size[0]
height = SCALE_FACTOR * map_size[1]

fps = 60.0



# Asks for user input in regards to the population of the species
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


if __name__ == '__main__':
    print("Hello, welcome to our aquarium simulator!")
    
    n_fishes = requestInput(name="fishes", default=60)
    n_sharks = requestInput(name="sharks", default=1)
    n_plankton = requestInput(name="plankton", default=100)

    print("\n===============================")  
    print("Fish initial population: " + str(n_fishes))
    print("Shark initial population: " + str(n_sharks))
    print("Plankton initial population: " + str(n_plankton))
    print("===============================\n")


    pg.init()
    pg.display.set_caption('')

    # Set up the window.
    screen = pg.display.set_mode((width, height))
    fpsClock = pg.time.Clock()
    screen.fill((255, 255, 255))

    env = Environment(
        canvas_shape=(width, height), \
        n_fishes=n_fishes, n_sharks=n_sharks, n_plankton=n_plankton,\
        max_steps=1000\
    )


    dt = 1/fps

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit() 
                sys.exit()

        # clear screen
        screen.fill((255, 255, 255))

        # update and draw env
        env.update(dt, params)
        env.draw(screen)

        pg.display.flip()        

        dt = fpsClock.tick(fps)


    
