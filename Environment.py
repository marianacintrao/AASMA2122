from turtle import update
import numpy as np
from Flocking import flock_forces
import math
import resources.consts as consts
import random
from Fish import Fish
from Shark import Shark
from Plankton import Plankton
from resources.agent import Agent
from resources.consts import PLANKTON_REPRODUCTION_RADIUS, PLANKTON_REPRODUCTION_RATE, SCALE_FACTOR, FISH_EAT, FISH_DIE


import pygame as pg


#from resources.consts import width, height

 
fishes = []
sharks = []
plankton = []


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

        # self.fish_beliefs = []

        self.max_steps = max_steps
        self.map_size = [20, 15]

        self.fish_locals = np.empty((0))

        
        # CREATING FISHES
        self.fish_positions = np.random.rand(n_fishes, 2) * self.map_size
        self.fish_velocities = (np.random.rand(n_fishes, 2) * 2) - 1

        for i in range(n_fishes):
            self.fishes.append(Fish(velocity=self.fish_velocities[i], position=self.fish_positions[i]))
            # self.fish_beliefs.append([])


        # CREATING PLANKTON
        self.plankton_positions = np.random.rand(n_plankton, 2) * self.map_size

        for i in range(n_plankton):
            self.plankton.append(Plankton(position=self.plankton_positions[i]))

        # CREATING SHARKS
        self.shark_positions = []
        #for i in range(n_sharks):
        #    self.sharks.append(Shark(velocity=self.velocities[i], position=positions[i]))




    def update_flocks(self, dt, positions, velocities, params, map_size):

        f1, f2, f3, self.fish_locals = flock_forces(
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
        return velocities
        # positions = positions + velocities * dt * params['speed']
        # return positions, velocities

    def update(self, dt, params):

        
        flock_fish_velocities = self.update_flocks(dt, self.fish_positions, self.fish_velocities, params, self.map_size)
        
        # UPDATE FISHES
        dead_fishes = []
        new_fishes_pos = np.empty((0, 2))
        for i in range(self.n_fishes):
            fish_action = self.fishes[i].update(dt, params, 
                plankton_positions=self.plankton_positions, plankton=self.plankton, 
                flock_fish_velocity=flock_fish_velocities[i], shark_positions=self.shark_positions, 
                fish_positions=self.fish_positions,
                fish_locals=self.fish_locals[i]
                )
            
            if fish_action == consts.FISH_EAT:
                # delete dead plankton
                plankton_id = self.fishes[i].closest_food_id
                self.n_plankton -= 1
                self.plankton_positions = np.delete(self.plankton_positions, plankton_id, axis=0)
                del self.plankton[plankton_id]
            elif fish_action == consts.FISH_DIE:
                # keep list of dead fishes
                dead_fishes.append(i)
            elif fish_action == consts.FISH_REPRODUCE:
                print("new poss", self.fishes[i].spawn_positions)
                new_fishes_pos = np.append(new_fishes_pos, self.fishes[i].spawn_positions, axis=0)

        # delete dead fishes
        self.fish_positions = np.delete(self.fish_positions, dead_fishes, axis=0)
        self.fish_velocities = np.delete(self.fish_velocities, dead_fishes, axis=0)
        self.n_fishes -= len(dead_fishes)
        self.fishes = [i for j, i in enumerate(self.fishes) if j not in dead_fishes]

        # create new fishes
        new_fishes_vel = (np.random.rand(len(new_fishes_pos), 2) * 2) - 1
        for i in range(len(new_fishes_pos)):
            self.fishes.append(Fish(velocity=new_fishes_vel[i], position=new_fishes_pos[i]))
        self.fish_positions = np.append(self.fish_positions, new_fishes_pos, axis=0)
        self.fish_velocities = np.append(self.fish_velocities, new_fishes_vel, axis=0)
        self.n_fishes += len(new_fishes_pos)

    
        
        for i in range(self.n_fishes):
            self.fish_velocities[i] = self.fishes[i].getVelocity()
            self.fish_positions[i] = self.fishes[i].getPosition()

        
        # UPDATE PLANKTON

        spawn = random.random() < PLANKTON_REPRODUCTION_RATE
        
        if spawn:
            random_plankton = np.random.randint(0, self.n_plankton)
            position = self.plankton[random_plankton].getPosition()
            min_x = position[0] - PLANKTON_REPRODUCTION_RADIUS
            max_x = position[0] + PLANKTON_REPRODUCTION_RADIUS
            min_y = position[1] - PLANKTON_REPRODUCTION_RADIUS
            max_y = position[1] + PLANKTON_REPRODUCTION_RADIUS
            new_plankton_pos =  np.array([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])

            self.plankton.append(Plankton(position=new_plankton_pos))
            self.plankton_positions = np.append(self.plankton_positions, [new_plankton_pos], axis=0)
            self.n_plankton += 1



    def draw(self, screen):
        for i in range(self.n_plankton):
            self.plankton[i].draw(screen, consts.PLANKTON_SIZE)
            
        for i in range(self.n_fishes):
            #self.fishes[i].draw(screen, self.fish_positions[i]*SCALE_FACTOR, consts.FISH_SIZE)
            self.fishes[i].draw(screen, consts.FISH_SIZE)
        
         

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

        