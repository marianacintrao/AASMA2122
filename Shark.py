import numpy as np
from resources.agent import Agent
from Fish import Fish
from resources.consts import energy_to_color


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

    def __init__(self, position: tuple):
        super(Agent, self).__init__(f"Shark")
        # self.energy = 100
        # self.color = energy_to_color(self.energy)
       
    def action(self) -> int:
        raise NotImplementedError()

