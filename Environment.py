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
from resources.consts import PLANKTON_REPRODUCTION_RADIUS, PLANKTON_REPRODUCTION_RATE, SCALE_FACTOR, FISH_EAT, FISH_DIE, FISH_REPRODUCTION_RADIUS, SHARK_VISION_RADIUS


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
        self.shark_positions = np.random.rand(n_sharks, 2) * self.map_size
        self.shark_velocities = (np.random.rand(n_sharks, 2) * 2) - 1
        for i in range(n_sharks):
            self.sharks.append(Shark(velocity=self.shark_velocities[i], position=self.shark_positions[i]))




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

        return velocities

    def updateFishes(self, dt, flock_fish_velocities, params):

        # get local fishes for reproduction
        distance = np.linalg.norm(self.fish_positions - self.fish_positions[:,None], axis=-1)
        local = distance < FISH_REPRODUCTION_RADIUS
        
        dead_fishes = []
        new_fishes_pos = np.empty((0, 2))
        for i in range(self.n_fishes):
            fish_action = self.fishes[i].update(dt, params, 
                plankton_positions=self.plankton_positions, plankton=self.plankton, 
                flock_fish_velocity=flock_fish_velocities[i], 
                shark_velocities=self.shark_velocities, shark_positions=self.shark_positions, 
                fish_positions=self.fish_positions,
                fish_locals=local[i]
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
                new_fishes_pos = np.append(new_fishes_pos, self.fishes[i].spawn_positions, axis=0)

        if len(dead_fishes) > 0:
            self.handle_fish_deaths(dead_fishes)

        # create new fishes
        new_fishes_vel = (np.random.rand(len(new_fishes_pos), 2) * 2) - 1
        for i in range(len(new_fishes_pos)):
            self.fishes.append(Fish(velocity=new_fishes_vel[i], position=new_fishes_pos[i]))
        self.fish_positions = np.append(self.fish_positions, new_fishes_pos, axis=0)
        self.fish_velocities = np.append(self.fish_velocities, new_fishes_vel, axis=0)
        self.n_fishes += len(new_fishes_pos)

        # update fish velocity and position vectors 
        for i in range(self.n_fishes):
            self.fish_velocities[i] = self.fishes[i].getVelocity()
            self.fish_positions[i] = self.fishes[i].getPosition()

    def updatePlankton(self):
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

    def updateSharks(self, dt, params):
        # get local fishes for reproduction

        #     s1  s2  f1  f2  f3
        # s1  t   f   t   f   f  
        # s2  f   f   f   f   f
        # f1  f   f   t   t   f
        # f2  f   f   t   t   f
        # f3  f   f   f   f   f

        sharks_and_fishes_pos = np.append(self.shark_positions, self.fish_positions, axis=0)
        distance_matrix = np.linalg.norm(sharks_and_fishes_pos - sharks_and_fishes_pos[:,None], axis=-1)

        dead_sharks = []
        new_sharks_pos = np.empty((0, 2))
        for i in range(self.n_sharks):

            shark_action = self.sharks[i].update(dt, distance_matrix=distance_matrix, n_sharks=self.n_sharks, id=i, fish_positions=self.fish_positions)

            
            if shark_action == consts.SHARK_EAT:
                # delete dead fishes
                fish_id = self.sharks[i].closest_food_id
                self.handle_fish_deaths([fish_id])
                # self.n_fishes -= 1
                # self.fish_positions = np.delete(self.fish_positions, fish_id, axis=0)
                # del self.fish[fish_id]
                break
            elif shark_action == consts.SHARK_DIE:
               dead_sharks.append(i)
            elif shark_action == consts.SHARK_REPRODUCE:
                new_sharks_pos = np.append(new_sharks_pos, self.sharks[i].spawn_positions, axis=0)
                break


        # delete dead sharks
        if len(dead_sharks) > 0:
            self.shark_positions = np.delete(self.shark_positions, dead_sharks, axis=0)
            self.shark_velocities = np.delete(self.shark_velocities, dead_sharks, axis=0)
            self.n_sharks -= len(dead_sharks)
            self.sharks = [i for j, i in enumerate(self.sharks) if j not in dead_sharks]
       
        # create new sharks
        new_sharks_vel = (np.random.rand(len(new_sharks_pos), 2) * 2) - 1
        for i in range(len(new_sharks_pos)):
            self.sharks.append(Shark(velocity=new_sharks_vel[i], position=new_sharks_pos[i]))
        self.shark_positions = np.append(self.shark_positions, new_sharks_pos, axis=0)
        self.shark_velocities = np.append(self.shark_velocities, new_sharks_vel, axis=0)
        self.n_sharks += len(new_sharks_pos)

        # update shark velocity and position vectors 
        for i in range(self.n_sharks):
            self.shark_velocities[i] = self.sharks[i].getVelocity()
            self.shark_positions[i] = self.sharks[i].getPosition()



    def update(self, dt, params):

        # GET FLOCK VELOCITY VECTORS
        flock_fish_velocities = self.update_flocks(dt, self.fish_positions, self.fish_velocities, params, self.map_size)
        
        # UPDATE FISHES
        self.updateFishes(dt, flock_fish_velocities, params)
        
        # UPDATE PLANKTON
        self.updatePlankton()

        # UPDATE SHARKS
        self.updateSharks(dt, params)
        


    def draw(self, screen):
        for i in range(self.n_plankton):
            self.plankton[i].draw(screen, consts.PLANKTON_SIZE)
            
        for i in range(self.n_fishes):
            self.fishes[i].draw(screen, consts.FISH_SIZE)

        for i in range(self.n_sharks):
            self.sharks[i].draw(screen, consts.SHARK_SIZE)
        
    def handle_fish_deaths(self, dead_fishes):
        # delete dead fishes
        self.fish_positions = np.delete(self.fish_positions, dead_fishes, axis=0)
        self.fish_velocities = np.delete(self.fish_velocities, dead_fishes, axis=0)
        self.n_fishes -= len(dead_fishes)
        if len(dead_fishes) > 1:
            self.fishes = [i for j, i in enumerate(self.fishes) if j not in dead_fishes]
        else:
            del self.fishes[dead_fishes[0]]



        