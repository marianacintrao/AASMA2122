import numpy as np
from Flocking import flock_forces
import math
import resources.consts as consts
from Fish import Fish
from Shark import Shark
from Plankton import Plankton
from resources.agent import Agent

import pygame as pg


#from resources.consts import width, height

 
fishes = []
sharks = []
plankton = []

SCALE_FACTOR = 50

#width = SCALE_FACTOR * map_size[0]
#height = SCALE_FACTOR * map_size[1]


class Environment():

    def __init__(self, n_fishes, n_sharks, n_plankton,
                 canvas_shape,
                 max_steps=100):
        self.canvas_shape = canvas_shape
        self.n_fishes = n_fishes
        self.positions = 0
        self.n_sharks = n_sharks
        self.n_plankton = n_plankton

        self.fishes = []
        self.plankton = []
        self.sharks = []

        self.max_steps = max_steps
        self.map_size = [20, 15]

        
        # CREATING FISHES
        self.fish_positions = np.random.rand(n_fishes, 2) * self.map_size
        self.fish_velocities = (np.random.rand(n_fishes, 2) * 2) - 1

        for i in range(n_fishes):
            self.fishes.append(Fish(velocity=self.fish_velocities[i], position=self.fish_positions[i], id=i))


        # CREATING PLANKTON
        self.plankton_positions = np.random.rand(n_plankton, 2) * self.map_size
        
        for i in range(n_plankton):
            self.plankton.append(Plankton(position=self.plankton_positions[i], id=i))

        # CREATING SHARKS
        #for i in range(n_sharks):
        #    self.sharks.append(Shark(velocity=self.velocities[i], position=positions[i]))




    def update_flocks(self, dt, positions, velocities, params, map_size):

        f1, f2, f3 = flock_forces(
            positions, velocities,
            map_size = map_size,
            **params
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

        #positions = positions + velocities * dt * consts.FISH_SPEED
        positions = positions + velocities * dt * params['speed']
        return positions, velocities

    def update(self, dt, params):
        # these are the positions and velocities for the fish, ONLY CONSIDERING THE SHOAL MOVEMENT
       
        f1, f2, f3 = flock_forces(
            self.fish_positions, self.fish_velocities,
            map_size = self.map_size,
            **params
        )

        

        # Need to limit the speeds here somehow since the forces returned
        # don't limit speed
        self.fish_velocities = self.fish_velocities + (f1 + f2 + f3) * dt
        # There has to be a better way of doing this bit, but this is speed
        # setting, ensuring all boids have unit speed (otherwise things tend to
        # go rather crazy)
        for v in range(self.n_fishes):
            self.fish_velocities[v, :] = (self.fish_velocities[v, :] / 
                np.linalg.norm(self.fish_velocities[v, :]))

        #positions = positions + velocities * dt * consts.FISH_SPEED
        self.fish_positions = self.fish_positions + self.fish_velocities * dt * params['speed']

        for i in range(self.n_fishes):
            self.fishes[i].update()





    def draw(self, screen):
        for i in range(self.n_plankton):
            self.plankton[i].draw(screen, self.plankton_positions[i]*SCALE_FACTOR, consts.PLANKTON_SIZE)
            
        for i in range(self.n_fishes):
            self.fishes[i].draw(screen, self.fish_positions[i]*SCALE_FACTOR, consts.FISH_SIZE)
        
         

    # Check if the fish is getting closer to the shark
    def check_Proximity(self, fish):
        maximumDistance = 10
        for i in self._n_sharks:
            distance = math.dist(fish.getPosition(),self._sharks[i].getPosition())
            # If the fish is too closed, returns True and the shark that is close
            if maximumDistance < distance:
                return True, self._sharks[i]
        # If the fish isn't close to other sharks, maintains the velocity
        return False, fish

    # Get velocity that represents the change in direction due to shark proximity
    def calculate_Velocity(self, fish, shark):
        # This returns the vector between both velocities
        return np.cross(fish.getVelocity(), shark.getVelocity())

    #def update(self, dt):
        #TODO
        # collects observations and gives out actions

        #generic movement
        #for i in self._n_fishes:
        #    # close2shark, agent = check_Proximity(self._fishes[i])
        #    # if close2shark: calculate_Velocity (self._fishes[i], agent)
        #    # With this new velocity the fish position is updated
        #    self._fishes[i].update(dt)
        #for i in self._n_sharks:
        #    self._sharks[i].update(dt)

    # def draw(self, screen):
    #     #TODO
    #     # draws all agents on the screen
    #     for i in range(self.n_fishes):
    #         self.fishes[i].move()
    #         color = slef.fishes[i].energy_to_color()
    #         pg.draw.circle(screen, color, fish_positions[i], consts.FISH_SIZE)

        