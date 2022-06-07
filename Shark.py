from resources.agent import Agent
from Fish import Fish
import pygame as pg
from resources.consts import SHARK_SIZE

class Shark(Fish):

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

    def __init__(self, position: tuple, velocity: list):
        super(Shark, self).__init__(position=position, velocity=velocity)
        self.name="Shark"
       
    def action(self) -> int:
        raise NotImplementedError()

    def draw(self, screen, p):
        color = self.getColor()
        radius = SHARK_SIZE
        pg.draw.circle(screen, color, p, radius)

    def eat(self, fish):
        # self.energy = fish.nutritional_value
        raise NotImplementedError()



