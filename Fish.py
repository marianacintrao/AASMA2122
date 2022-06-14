from asyncio.windows_events import NULL
from turtle import position
import numpy as np
import pygame as pg
# from Environment import SCALE_FACTOR
from resources.agent import Agent
from resources.consts import FISH_MAX_ENERGY
from resources.consts import SCALE_FACTOR
from resources.consts import FISH_SIZE
from resources.consts import energy_to_color
from resources.consts import influence_prox
from Flocking import flock_forces
from colour import Color
import math



FISH_INTENTIONS = 5
FISH_GO_TO_PLANKTON, FISH_EAT, ESCAPE, FISH_REPRODUCE, FLOCK = range(FISH_INTENTIONS)


class Fish(Agent):

    """
    Fish class.
    Represents the concept of a fish agent.



    """



    def __init__(self, velocity, position):
    # def __init__(self, position: tuple, velocity: list):
        super(Fish, self).__init__(f"Fish")
        self.energy = FISH_MAX_ENERGY

        self.energy_decrease = 1
        self.nutritional_value = FISH_MAX_ENERGY // 20
        self.can_reproduce = False

        self.vision_radius = influence_prox / 10

        self.velocity = velocity
        self.position = position
        
        self.belief = {'SHARK': False, 'FOOD': False, 'MATE': False}

        self.closest_food_id = None
        self.closest_food_distance = None
        

    def getColor(self) -> tuple:
        return energy_to_color(self.energy)

    def getPosition(self) -> list:
        return self.position

    def getVelocity(self) -> list:
        return self.velocity

    # updates beliefs
    def observe(self, plankton_positions, shark_positions=[], fish_positions=[]):

        # check plankton proximity
        dist = []
        for plankton_position in plankton_positions:
            dist.append(np.linalg.norm(self.position - plankton_position))

        closest_food_distance = min(dist)

        if closest_food_distance <= self.vision_radius:
            self.belief["FOOD"] = True
            self.closest_food_distance = closest_food_distance
            self.closest_food_id = dist.index(closest_food_distance)

        # check shark proximity

        # check other fish proximity

    # returns an intention
    def deliberate(self) -> int:

        energy = self.energy
        belief = self.belief
    
        if energy < FISH_MAX_ENERGY * .5 and belief['FOOD']:
            if self.closest_food_distance < self.vision_radius * .5:
                return FISH_EAT
            else:
                return FISH_GO_TO_PLANKTON # intends to eat
        else:
            return FLOCK # default case (fish just vibes)

                    
    def eat(self, plankton_positions, plankton):

        self.energy += plankton[self.closest_food_id].nutricional_value

        return self.closest_food_id

    def energy_to_color(self) -> tuple:
        # returns rgb tuple
        return energy_to_color(self.energy)
        
    def action(self, eat=None, reproduce=None, move=None) -> int:
        raise NotImplementedError()

    def draw(self, screen, r):
        color = energy_to_color(self.energy)
        pg.draw.circle(screen, color, (self.position[0]* SCALE_FACTOR, self.position[1]* SCALE_FACTOR), r)

    # def reset_belief()


    def update(self, dt, params, plankton_positions, plankton, flock_fish_velocity, shark_positions=[], fish_positions=[]):
        #self.move()
        plankton_ate = None
        self.observe(plankton_positions, shark_positions, fish_positions)
        intention = self.deliberate()
        if intention == FLOCK:
            self.move(dt, params, flock_fish_velocity)
        elif intention == FISH_GO_TO_PLANKTON:
            self.move_to_plankton(dt, params, plankton_positions[self.closest_food_id])
        elif intention == FISH_EAT:
            print("EAT")
            plankton_ate = self.eat(plankton_positions, plankton)



        self.closest_food_id = None
        self.closest_food_distance = None
        self.belief['FOOD'] = False
        return plankton_ate


    def move(self, dt, params, velocity):
        self.position = self.position + velocity * dt * params['speed']
        self.velocity = velocity
        self.energy = self.energy - self.energy_decrease


    def move_to_plankton(self, dt, params, plankton_pos):
        
        velocity = plankton_pos - self.position
        np.linalg.norm(velocity)

        self.move(dt, params, velocity)

    
    # def peerDistance(self, fish):
    #     p1 = self.position
    #     p2 = fish.position
    #     distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
    #     return distance




    

