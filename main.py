from msilib.schema import Environment
import string
import sys
import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from Fish import Fish
from Shark import Shark
from resources.agent import Agent
from Environment import Environment as Env
import resources.consts as consts


SCALE_FACTOR = 1
width, height = (1000, 500)
fps = 60.0

fishes = []
sharks = []
plankton = []


# def render_text(screen, what, color, where):
#     font = pg.font.SysFont('monospace', 20)
#     text = font.render(str(what), 1, pg.Color(color))
#     screen.blit(text, where)

# Creates the chosen ammount of fishes in an initial random position on the screen
def createFishes(n_fishes):
    for _ in range(n_fishes):
        fish_velocity = (np.random.rand(1, 2) * consts.FISH_SPEED * 2) - consts.FISH_SPEED
        fish_velocity = (fish_velocity[0,0], fish_velocity[0,1]
        )
        fish_position = (np.random.rand(1, 2)).dot( \
                        np.array([[width, 0], \
                        [0, height]]) ) 
        fish_position = (fish_position[0,0], fish_position[0,1])

        fishes.append(Fish(position=fish_position, velocity=fish_velocity))


# Creates the chosen ammount of sharks in an initial random position on the screen
def createFishes(n_sharks):
    for _ in range(n_sharks):
        shark_velocity = (np.random.rand(1, 2) * consts.SHARK_SPEED * 2) - consts.SHARK_SPEED
        shark_velocity = (shark_velocity[0,0], shark_velocity[0,1]
        )
        shark_position = (np.random.rand(1, 2)).dot( \
                        np.array([[width, 0], \
                        [0, height]]) ) 
        shark_position = (shark_position[0,0], shark_position[0,1])

        sharks.append(Shark(position=shark_position, velocity=shark_velocity))


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

def run_single_agent(environment: Env, agent: Agent, n_episodes: int) -> np.ndarray:

    results = np.zeros(n_episodes)

    for episode in range(n_episodes):

        steps = 0
        terminal = False
        observation = environment.reset()
        while not terminal:
            steps += 1
            # TODO - Main Loop (4 lines of code)
            agent.see(observation)
            action = agent.action()
            next_obs, reward, terminal, info = environment.step(action)
            observation = next_obs

        environment.close()

        results[episode] = steps

    return results


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

    # # fishList = [Fish() for i in range(n_fishes)]
    # env = Environment()

    createFishes(n_fishes)

    # env = Environment(
    #      canvas_shape=(width, height),
    #      n_fishes=20, n_sharks=1, n_plankton=50,
    #      max_steps=1000
    #  )


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

    print(sharks[0].name, sharks[0].energy)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit() 
                sys.exit()

        # # Clear screen
        screen.fill((255, 255, 255))

        # positions, velocities = env.update(dt, positions, velocities, params)
        # env.draw(screen, positions*SCALE_FACTOR, (100, 100, 200), 5)
        # env.update(dt)
        # env.draw(screen, positions*SCALE_FACTOR, (100, 100, 200), 5)
        pg.display.update()

        dt = fpsClock.tick(fps)


    
