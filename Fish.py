import numpy as np
from resources.agent import Agent
from resources.consts import energy_to_color


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

    def __init__(self, position: tuple, velocity: list):
    # def __init__(self, position: tuple, velocity: list):
        super(Agent, self).__init__(f"Fish")
        self.energy = 100
        self.color = energy_to_color(self.energy)
        self.can_reproduce = False
        self.position = position
        self.velocity = np.array(velocity) 

    def getColor() -> tuple:
        return energy_to_color(self.energy)

    def getPosition() -> tuple:
        return self.position
        
    def action(self, eat=None, reproduce=None, move=None) -> int:
        raise NotImplementedError()

    

