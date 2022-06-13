from asyncio.windows_events import NULL
import numpy as np
import pygame as pg
from resources.agent import Agent
from resources.consts import FISH_MAX_ENERGY
from resources.consts import FISH_SIZE
from resources.consts import energy_to_color
from Flocking import flock_forces
from colour import Color
import math

class Fish(Agent):

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

    def __init__(self, velocity, position, id):
    # def __init__(self, position: tuple, velocity: list):
        super(Fish, self).__init__(f"Fish")
        self.energy = FISH_MAX_ENERGY
        # self.energy_decrease = FISH_MAX_ENERGY // 100
        self.energy_decrease = 1
        self.nutritional_value = FISH_MAX_ENERGY // 20
        self.can_reproduce = False

        self.velocity = velocity
        self.position = position

        self.id = id

    def getColor(self) -> tuple:
        return energy_to_color(self.energy)

    def getPosition(self) -> tuple:
        return self.position

    def getVelocity(self) -> tuple:
        return self.velocity

    def eat(self, plankton):
        # self.energy += plankton.nutritional_value
        raise NotImplementedError()

    def energy_to_color(self) -> tuple:
        # returns rgb tuple
        return energy_to_color(self.energy)
        
    def action(self, eat=None, reproduce=None, move=None) -> int:
        raise NotImplementedError()

    def draw(self, screen, p, r):
        color = energy_to_color(self.energy)
        pg.draw.circle(screen, color, p, r)

    def update(self):
        self.move()

    # def move(self, position, velocity):
    def move(self):
        self.energy = self.energy - self.energy_decrease
        # self.position = position
        # self.velocity = velocity
        # raise NotImplementedError()
    
    # def peerDistance(self, fish):
    #     p1 = self.position
    #     p2 = fish.position
    #     distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
    #     return distance

    

    
# def flocking(a: Fish, b: Fish):




    

