from asyncio.windows_events import NULL
from turtle import position
import numpy as np
import pygame as pg
# from Environment import SCALE_FACTOR
from resources.agent import Agent
from resources.consts import FISH_MAX_ENERGY, FISH_REPRODUCTION_RATE, FISH_REPRODUCTION_RADIUS
from resources.consts import SCALE_FACTOR
from resources.consts import FISH_SIZE
from resources.consts import energy_to_color
from resources.consts import influence_prox
import resources.consts as consts
from Flocking import flock_forces
from colour import Color
import random
import math





class Fish(Agent):

    """
    Fish class.
    Represents the concept of a fish agent.

    """

    def __init__(self, velocity, position):
        super(Fish, self).__init__(f"Fish")
        self.energy = FISH_MAX_ENERGY

        self.energy_decrease = 1
        self.nutritional_value = FISH_MAX_ENERGY // 20
        self.reproduction_rate = consts.FISH_REPRODUCTION_RATE
        self.reproduction_radius = consts.FISH_REPRODUCTION_RADIUS


        self.vision_radius = influence_prox // 1

        self.velocity = velocity
        self.position = position
        
        self.belief = {'SHARK': False, 'FOOD': False, 'MATE': False}

        self.closest_food_id = None
        self.closest_food_distance = None

        self.spawn_positions = None
  

    def getColor(self) -> tuple:
        return energy_to_color(self.energy)

    def getPosition(self) -> list:
        return self.position

    def getVelocity(self) -> list:
        return self.velocity

    # updates beliefs
    def observe(self, plankton_positions, shark_positions=[], fish_positions=[], fish_locals=[]):

        # check plankton proximity
        if len(plankton_positions) > 0:
            
            planktonDist = []
            for plankton_position in plankton_positions:
                planktonDist.append(np.linalg.norm(self.position - plankton_position))
    
            closest_food_distance = min(planktonDist)
    
            if closest_food_distance <= self.vision_radius:
                self.belief["FOOD"] = True
                self.closest_food_distance = closest_food_distance
                self.closest_food_id = planktonDist.index(closest_food_distance)

       # # check shark proximity
       # dangerDist = []
       # for shark_position in plankton_positions:
       #     dangerDist.append(np.linalg.norm(self.position - shark_position))

       # check for available fishes to reproduce:
        countTrue = np.count_nonzero(fish_locals)
        if countTrue > 0:
            self.belief['MATE'] = countTrue

    # returns an intention
    def deliberate(self) -> int:

        energy = self.energy
        belief = self.belief
        if energy > FISH_MAX_ENERGY * .5 and belief['MATE']:
            return consts.FISH_REPRODUCE
        elif energy < self.energy_decrease:
            return consts.FISH_DIE
        elif energy < FISH_MAX_ENERGY * .5 and belief['FOOD']:
            if self.closest_food_distance < self.vision_radius * .05:
                return consts.FISH_EAT
            else:
                return consts.FISH_GO_TO_PLANKTON # intends to eat
        else:
            return consts.FLOCK # default case (fish just vibes)

    def reproduce(self):
        # spawn = random.random() < self.reproduction_rate
        self.spawn_positions = np.empty((0, 2))
        if random.random() < FISH_REPRODUCTION_RATE:
            for _ in range(self.belief['MATE']):
                self.energy -= consts.FISH_MAX_ENERGY // 30
                min_x = self.position[0] - self.reproduction_radius
                max_x = self.position[0] + self.reproduction_radius
                min_y = self.position[1] - self.reproduction_radius
                max_y = self.position[1] + self.reproduction_radius
                pos = np.array([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
                self.spawn_positions = np.append(self.spawn_positions, [pos], axis=0)
                if self.energy < consts.FISH_MAX_ENERGY * .5:
                    break        
                    
    def eat(self, plankton_positions, plankton):
        self.energy += plankton[self.closest_food_id].nutricional_value


    def energy_to_color(self) -> tuple:
        # returns rgb tuple
        return energy_to_color(self.energy)
        
    def action(self, eat=None, reproduce=None, move=None) -> int:
        raise NotImplementedError()

    def draw(self, screen, r):
        color = energy_to_color(self.energy)
        pg.draw.circle(screen, color, (self.position[0]* SCALE_FACTOR, self.position[1]* SCALE_FACTOR), r)

    def reset_belief(self):
        self.closest_food_id = None
        self.closest_food_distance = None
        self.spawn_positions = None
        self.belief['FOOD'] = False
        self.belief['SHARK'] = False
        self.belief['MATE'] = False


    def update(self, dt, params, plankton_positions, plankton, flock_fish_velocity, shark_positions=[], fish_positions=[], fish_locals=[]):

        self.reset_belief()

        self.observe(plankton_positions, shark_positions, fish_positions, fish_locals)

        intention = self.deliberate()
        if intention == consts.FISH_DIE:
            return consts.FISH_DIE
        elif intention == consts.FLOCK:
            self.move(dt, params, flock_fish_velocity)
            return consts.FLOCK
        elif intention == consts.FISH_GO_TO_PLANKTON:
            self.move_to_plankton(dt, params, plankton_positions[self.closest_food_id])
            return consts.FISH_GO_TO_PLANKTON
        elif intention == consts.FISH_EAT:
            self.eat(plankton_positions, plankton)
            return consts.FISH_EAT
        elif intention == consts.FISH_REPRODUCE:
            self.reproduce()
            self.move(dt, params, flock_fish_velocity)
            return consts.FISH_REPRODUCE


    def move(self, dt, params, velocity):
        self.position = self.position + velocity * dt * params['speed']
        self.velocity = velocity

        self.energy = self.energy - self.energy_decrease 


    def move_to_plankton(self, dt, params, plankton_pos):
        
        velocity = plankton_pos - self.position
        
        # np.linalg.norm(velocity)

        self.move(dt, params, velocity)
    

