from msilib.schema import Environment
from resources.consts import map_size
import string
import sys
import numpy as np
import os
import pygame as pg
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots, savefig
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from resources.utils import plot_confidence_bar


from Environment import Environment
import resources.consts as consts
#from resources.consts import width, height 

N_RUNS = 3

params = {
    'speed': consts.FISH_SPEED,
    'influence_prox': consts.influence_prox,
    'alignment_factor': 0.005,
    'cohesion_factor': 0.005,
    'separation_factor': 0.0002
}


SCALE_FACTOR = 50

width = SCALE_FACTOR * map_size[0]
height = SCALE_FACTOR * map_size[1]

fps = 60.0


fish_population = []
fish_deaths = []
fish_births = []
shark_population = []
shark_deaths = []
shark_births = []
plankton_population = []
plankton_deaths = []
plankton_births = []

it_interval = 30
n_datapoints = 15

max_it = it_interval * n_datapoints
fish_pop = []
plankton_pop = []
shark_pop = []

newborn_fishes = []
newborn_plankton = []
newborn_sharks = []

dead_fishes = []
dead_plankton = []
dead_sharks = []

starved_fishes = 0
predated_fishes = 0

starved_fishes_per_test = []
predated_fishes_per_test = []

fig = plt.figure(figsize=(8, 6))

def update_metrics(env, i):
    print("=========\niteration:", i//it_interval,"\n=========")
    
    n_fishes, n_plankton, n_sharks = env.get_population_metrics()
    print("n_fishes, n_plankton, n_sharks:", n_fishes, n_plankton, n_sharks)

    fish_pop.append(n_fishes)
    plankton_pop.append(n_plankton)
    shark_pop.append(n_sharks)

    baby_fishes, baby_plankton, baby_sharks = env.get_n_newborns()
    print("baby_fishes, baby_plankton, baby_sharks:", baby_fishes, baby_plankton, baby_sharks)
    newborn_fishes.append(baby_fishes)
    newborn_plankton.append(baby_plankton)
    newborn_sharks.append(baby_sharks)

    fish_deaths, plankton_deaths, shark_deaths = env.get_n_deaths()
    print("fish_deaths, plankton_deaths, shark_deaths:", fish_deaths, plankton_deaths, shark_deaths)
    dead_fishes.append(fish_deaths)
    dead_plankton.append(plankton_deaths)
    dead_sharks.append(shark_deaths)
    
    s, p = env.fish_death_types()
    global starved_fishes
    global predated_fishes
    starved_fishes += s
    predated_fishes += p



def draw_population_metrics():
    t = range(0, n_datapoints)
    fishes = fish_pop
    plankton = plankton_pop
    sharks = shark_pop

    ax = plt.subplot(221)
    ax.set_title("Population evolution")
    ax.plot(t, plankton, 'r', label='Number of Plankton')
    ax.plot(t, sharks, 'b', label="Number of Sharks")
    ax.plot(t, fishes, 'g', label='Number of Fishes')
    ax.legend()



def draw_newborn_metrics():
    t = range(0, n_datapoints)
    fishes = newborn_fishes
    plankton = newborn_plankton
    sharks = newborn_sharks


    ax = plt.subplot(222)
    ax.set_title("Newborn agents")
    ax.plot(t, plankton, 'r', label='Newborn Plankton')
    ax.plot(t, sharks, 'b', label='Newborn Sharks')
    ax.plot(t, fishes, 'g', label='Newborn Fishes')
    ax.legend()


def draw_dead_metrics():
    t = range(0, n_datapoints)
    fishes = dead_fishes
    plankton = dead_plankton
    sharks = dead_sharks


    ax = plt.subplot(223)
    ax.set_title("Dead agents")
    ax.plot(t, plankton, 'r', label='Dead Plankton')
    ax.plot(t, sharks, 'b', label='Dead Sharks')
    ax.plot(t, fishes, 'g', label='Dead Fishes')
    ax.legend()

def draw_death_types_metrics():
    t = range(0, n_datapoints)
    fishes = dead_fishes
    plankton = dead_plankton
    sharks = dead_sharks


    ax = plt.subplot(224)
    ax.set_title("Dead agents")
    ax.plot(t, plankton, 'r', label='Dead Plankton')
    ax.plot(t, sharks, 'b', label='Dead Sharks')
    ax.plot(t, fishes, 'g', label='Dead Fishes')
    ax.legend()

def draw_fish_death_types():

    # stds = [np.std([starved_fishes_per_test]), np.std(predated_fishes_per_test)]
    # print([starved_fishes, predated_fishes])
    plot_confidence_bar(
        names=["deaths by starvation", "deaths by predation"],
        # means=[sum(starved_fishes_per_test)/len(starved_fishes_per_test), sum(predated_fishes_per_test)/len(predated_fishes_per_test)],
        means=[starved_fishes, predated_fishes],
        # std_devs=stds,
        std_devs=[0, 0],
        # N=[N_RUNS,N_RUNS],
        N=[1,1],
        title="Causes of fish deaths",
        x_label="", y_label=f"Avg. {'total deaths'}",
        confidence=0.95, show=True, colors=None
    )


    
    
def run(env):
    pg.init()
    pg.display.set_caption('')

    # Set up the window.
    screen = pg.display.set_mode((width, height))
    fpsClock = pg.time.Clock()
    screen.fill((255, 255, 255))

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


def run_no_viz(env):

    fpsClock = pg.time.Clock()

    dt = 1/fps
    
    it_counter = 0

    while it_counter < max_it:
        # update env
        env.update(dt, params)
        if it_counter % it_interval == 0:
            update_metrics(env, it_counter)
        it_counter += 1

        dt = fpsClock.tick(fps)

    draw_population_metrics()
    draw_newborn_metrics()
    draw_dead_metrics()
    draw_fish_death_types()

    fig.tight_layout()
    fig.show()

# Asks for user input in regards to the population of the species
def requestInput(name: string, default: int):
    
    while True:
        inp = input("Enter number of %s, default is %d: " % (name, default))
        if not inp.strip():
            return default
            
        if not inp.isnumeric() or int(inp) < 0:
            print("Please enter an integer >= than 0")
            continue
        else:
            return int(inp)


if __name__ == '__main__':
    print("Hello, welcome to our aquarium simulator!")
    
    n_fishes = requestInput(name="fishes", default=60)
    n_sharks = requestInput(name="sharks", default=4)
    n_plankton = requestInput(name="plankton", default=100)

    visualize = False
    while True:
        inp = input("Do you want to visualize the simulation? If not, you'll get metrics (y/n, default is n): ")
        if not inp.strip() or inp == 'n':
            break   
        if inp == 'y':
            visualize = True
            break
        else:
            print("Please enter 'y' or 'n'")
            continue

    print("\n================================")  
    print("Fish initial population: " + str(n_fishes))
    print("Shark initial population: " + str(n_sharks))
    print("Plankton initial population: " + str(n_plankton))
    print("================================\n")

    env = Environment(
        canvas_shape=(width, height), \
        n_fishes=n_fishes, n_sharks=n_sharks, n_plankton=n_plankton,\
        max_steps=1000\
    )

    run(env) if visualize else run_no_viz(env)

    

   
    
