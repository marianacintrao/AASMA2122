from asyncio.windows_events import NULL
from turtle import position
import numpy as np
import pygame as pg
# from Environment import SCALE_FACTOR
from resources.agent import Agent
from resources.consts import SHARK_MAX_ENERGY, SHARK_REPRODUCTION_RATE, SHARK_REPRODUCTION_RADIUS, SHARK_ENERGY_FOR_REPRODUCING, SHARK_RATIO_FOR_REPRODUCING, SHARK_RADIUS_FOR_EATING, SHARK_SCARED_OF_N_FISHES, SHARK_VISION_RADIUS
from resources.consts import FISH_NUTRITIONAL_VALUE
from resources.consts import SCALE_FACTOR
from resources.consts import SHARK_SIZE
from resources.consts import shark_energy_to_color
from resources.consts import influence_prox
from resources.consts import map_size
from resources.consts import margin
import resources.consts as consts
import random

class Shark(Agent):

    """
    Fish class.
    Represents the concept of a fish agent.

    Attributes
    ----------
    color: tuple
        Color of the agent. It is linked to its energy (green -> full; red -> almost dead xD)
        
    Methods
    -------
    getColor(): tuple
        Returns the color of the agent, represented by a tuple

    """

    def __init__(self, velocity, position):
        super(Shark, self).__init__(f"Shark")
        self.energy = SHARK_MAX_ENERGY

        self.energy_decrease = 1
        self.nutritional_value = None
        self.reproduction_rate = consts.SHARK_REPRODUCTION_RATE
        self.reproduction_radius = consts.SHARK_REPRODUCTION_RADIUS

        self.vision_radius = influence_prox // 1

        self.velocity = velocity
        self.position = position
        
        self.belief = {'FOOD': False, 'MATE': False}

        self.closest_food_id = None
        self.closest_food_distance = None

        self.spawn_positions = None

        # self.fishes_distance = np.empty((0))

    def getPosition(self) -> tuple:
        return self.position

    def getVelocity(self) -> tuple:
        return self.velocity
       
    def action(self) -> int:
        raise NotImplementedError()

    def energy_to_color(self) -> tuple:
        # returns rgb tuple
        return shark_energy_to_color(self.energy)

    # returns an intention
    def deliberate(self) -> int:

        energy = self.energy
        belief = self.belief
        if energy > SHARK_MAX_ENERGY * SHARK_ENERGY_FOR_REPRODUCING and belief['MATE']:
            return consts.SHARK_REPRODUCE
        elif energy < self.energy_decrease:
            return consts.SHARK_DIE
        elif energy < SHARK_MAX_ENERGY - FISH_NUTRITIONAL_VALUE and belief['FOOD']:
            if self.closest_food_distance < self.vision_radius * SHARK_RADIUS_FOR_EATING:
                return consts.SHARK_EAT
            else:
                return consts.SHARK_GO_TO_FISH # intends to eat
        else:
            return consts.SHARK_MOVE # default case (fish just vibes)

    def observe(self, distance_matrix, n_sharks, id):

        ''' DISTANCE MATRIX SHAPE 
        #     s1  s2  f1  f2  f3
        # s1  t   f   t   f   f  
        # s2  f   f   f   f   f
        # f1  f   f   t   t   f
        # f2  f   f   t   t   f
        # f3  f   f   f   f   f
        '''
        sharks_distance = distance_matrix[0:n_sharks, 0:n_sharks]
        local_sharks = sharks_distance < SHARK_VISION_RADIUS * SHARK_RATIO_FOR_REPRODUCING

        fishes_distance = distance_matrix[id][n_sharks:]
        local_fishes = fishes_distance < SHARK_VISION_RADIUS

        n_fishes = local_fishes.shape[0]
        max_dist = np.max(fishes_distance)
        min_dist = np.min(fishes_distance)

        if np.count_nonzero(local_fishes) > 0:
            for i in range(n_fishes):
                if fishes_distance[i] == min_dist:
                    fish_locals = distance_matrix[i + n_sharks][n_sharks:] < SHARK_VISION_RADIUS
                    countTrue = np.count_nonzero(fish_locals)
                    if countTrue > SHARK_SCARED_OF_N_FISHES:
                        # this fish doesn't count
                        fishes_distance[i] = max_dist
                        min_dist = np.min(fishes_distance)
                    else:
                        self.belief['FOOD'] = countTrue
                        self.closest_food_id = i
                        self.closest_food_distance = fishes_distance[i]
                        # self.fishes_distance = fishes_distance 
                        break 
        # check for available sharks to reproduce:
        countTrue = np.count_nonzero(local_sharks)
        if countTrue > 0:
            self.belief['MATE'] = countTrue - 1
        


    def reset_belief(self):
        self.closest_food_id = None
        self.closest_food_distance = None
        self.spawn_positions = None
        self.belief['FOOD'] = False
        self.belief['MATE'] = False


    def update(self, dt, distance_matrix, n_sharks, id, fish_positions):

        self.reset_belief()

        self.observe(distance_matrix, n_sharks, id)

        intention = self.deliberate()
        if intention == consts.SHARK_DIE:
            return consts.SHARK_DIE
        elif intention == consts.FLOCK:
            self.move(dt, self.velocity)
            return consts.FLOCK
        elif intention == consts.SHARK_GO_TO_FISH:
            self.move_to_fish(dt, fish_positions[self.closest_food_id])
            # print("TA A ir po peixe")

            return consts.SHARK_GO_TO_FISH
        elif intention == consts.SHARK_EAT:
            self.eat()
            return consts.SHARK_EAT
        elif intention == consts.SHARK_REPRODUCE:
            self.reproduce()
            self.move(dt, self.velocity)
            return consts.SHARK_REPRODUCE

    def draw(self, screen, r):
        color = self.energy_to_color()
        pg.draw.circle(screen, color, (self.position[0]* SCALE_FACTOR, self.position[1]* SCALE_FACTOR), r)



    def reproduce(self):
        # spawn = random.random() < self.reproduction_rate
        self.spawn_positions = np.empty((0, 2))
        if random.random() < SHARK_REPRODUCTION_RATE:
            for _ in range(self.belief['MATE']):
                self.energy -= consts.SHARK_MAX_ENERGY // 30
                min_x = self.position[0] - self.reproduction_radius
                max_x = self.position[0] + self.reproduction_radius
                min_y = self.position[1] - self.reproduction_radius
                max_y = self.position[1] + self.reproduction_radius
                pos = np.array([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
                self.spawn_positions = np.append(self.spawn_positions, [pos], axis=0)
                if self.energy < consts.SHARK_MAX_ENERGY * .5:
                    break        
                    
                    
    def eat(self):
        print("TA A COMER")
        print("energia antes", self.energy)
        self.energy += FISH_NUTRITIONAL_VALUE
        print("energia depois", self.energy)

    def move(self, dt, velocity):

        self.position = self.position + velocity * dt * consts.SHARK_SPEED
        if self.position[0] > map_size[0] + margin:
            self.position[0] = 0 - margin
        elif self.position[0] < 0 - margin:
            self.position[0] = map_size[0] + margin
        if self.position[1] > map_size[1] + margin:
            self.position[1] = 0 - margin
        elif self.position[1] < 0 - margin:
            self.position[1] = map_size[1] + margin

        self.velocity = velocity
        self.energy = self.energy - self.energy_decrease 

    def move_to_fish(self, dt, fish_position):
        velocity = fish_position - self.position
        self.move(dt, velocity)




