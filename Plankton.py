import pygame as pg
from colour import Color
from resources.agent import Agent
from resources.consts import FISH_MAX_ENERGY
from resources.consts import SCALE_FACTOR



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
        self.nutricional_value = FISH_MAX_ENERGY // 10

        #self.id = id

    def getColor(self) -> tuple:
        # return energy_to_color(self.energy)
        return Color("green")
    
    def action(self):
        return None

    def getPosition(self) -> tuple:
        return self.position

    def reproduce(self):
        raise NotImplementedError()

    def draw(self, screen, r):
        p = self.position * SCALE_FACTOR
        pg.draw.circle(screen, (0,255,0), (p[0], p[1]), r)
