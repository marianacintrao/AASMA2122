import numpy as np
import pygame as pg
from resources.agent import Agent
from resources.consts import FISH_MAX_ENERGY
from resources.consts import FISH_SIZE
from resources.consts import energy_to_color
from Flocking import flock_forces


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
        super(Fish, self).__init__(f"Fish")
        self.energy = FISH_MAX_ENERGY
        self.energy_decrease = FISH_MAX_ENERGY / 100
        self.nutritional_value = FISH_MAX_ENERGY / 20
        # self.color = energy_to_color(self.energy)
        self.can_reproduce = False
        self.position = position
        self.velocity = np.array(velocity) 

        self.map_size = [20, 10]
        self.params = {
            'speed': 0.005,
            'influence_prox': 2,
            'alignment_factor': 0.003,
            'cohesion_factor': 0.003,
            'separation_factor': 0.0005
        }

    def getColor() -> tuple:
        return energy_to_color(self.energy)

    def getPosition() -> tuple:
        return self.position

    def eat(self, plankton):
        # self.energy += plankton.nutritional_value
        raise NotImplementedError()

    def energy_to_color(self, energy) -> tuple:
        return (100, 100, 100)
        
    def action(self, eat=None, reproduce=None, move=None) -> int:
        raise NotImplementedError()

    def draw(self, screen, p):
        color = self.getColor()
        radius = FISH_SIZE
        pg.draw.circle(screen, color, p, radius)

    def update(self, dt):
        #raise NotImplementedError()

        f1, f2, f3 = flock_forces(
            positions, velocities,
            map_size = self.map_size,
            **self.params
        )
        # Need to limit the speeds here somehow since the forces returned
        # don't limit speed
        velocities = velocities + (f1 + f2 + f3) * dt
        # There has to be a better way of doing this bit, but this is speed
        # setting, ensuring all boids have unit speed (otherwise things tend to
        # go rather crazy)
        for v in range(len(velocities)):
            velocities[v, :] = (velocities[v, :] / 
                np.linalg.norm(velocities[v, :]))
    
        positions = positions + velocities * dt * self.params['speed']
        return positions, velocities

    def move(self, position, velocity):
        self.energy = self.energy - self.energy_decrease
        self.position = position
        self.velocity = velocity
        raise NotImplementedError()


    

