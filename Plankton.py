import pygame as pg
import numpy as np
from colour import Color
from resources.agent import Agent
from resources.consts import FISH_MAX_ENERGY
from resources.consts import SCALE_FACTOR
from resources.consts import PLANKTON_REPRODUCTION_RATE
from resources.consts import PLANKTON_REPRODUCTION_RADIUS
import random



class Plankton(Agent):

    """
    Plankton class.
    Represents the concept of a (not very smart) plankton agent.

    Attributes
    ----------
    color: tuple
        Color of the agent. It is linked to its energy (green -> full; red -> almost dead xD)
        
    Methods
    -------
    getColor(): tuple
        Returns the color of the agent, represented by a tuple

    """

    def __init__(self, position):
    # def __init__(self, position: tuple, velocity: list):
        super(Plankton, self).__init__(f"Plankton")
        self.position = position
        self.nutricional_value = FISH_MAX_ENERGY // 2
        self.reproduction_rate = PLANKTON_REPRODUCTION_RATE
        self.reproduction_radius = PLANKTON_REPRODUCTION_RADIUS


    def getColor(self) -> tuple:
        return Color("green")
    
    def action(self):
        return None

    def getPosition(self) -> list:
        return self.position

    def reproduce(self) -> list:
        
        spawn = random.random() < self.reproduction_rate

        if spawn:
            min_x = self.position[0] - self.reproduction_radius
            max_x = self.position[0] + self.reproduction_radius
            min_y = self.position[1] - self.reproduction_radius
            max_y = self.position[1] + self.reproduction_radius
            return np.array([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        else:
            return None

    def update(self):
        return self.reproduce()

    def draw(self, screen, r):
        p = self.position * SCALE_FACTOR
        pg.draw.circle(screen, (0,255,0), (p[0], p[1]), r)
