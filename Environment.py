import numpy as np
from Flocking import flock_forces
 
class Environment():

    def __init__(self, n_fishes, n_sharks, n_plankton,
                 fishes, sharks, plankton,
                 max_steps=100, 
                 canvas_shape=(1000, 500)):
        self._canvas_shape = canvas_shape
        self._n_fishes = n_fishes
        self._n_sharks = n_sharks
        self._n_plankton = n_plankton
        self._fishes = fishes
        self._sharks = sharks
        self._plankton = plankton
        self._max_steps = max_steps

    def update_flocks(dt, fishes, params):

        positions = [fish.position for fish in fishes]
        velocities = [fish.velocity for fish in fishes]
        
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

        positions = positions + velocities * dt * params['speed']
        return positions, velocities



    def update(self, dt):
        #TODO
        # collects observations and gives out actions

        #generic movement
        for i in self._n_fishes:
            self._fishes[i].update(dt)
        for i in self._n_sharks:
            self._sharks[i].update(dt)

    def draw(self, screen):
        #TODO
        # draws all agents on the screen
        for i in self._n_fishes:
            self.fishes[i].draw(screen, (100, 100, 100), p, 5)
        for i in self._n_sharks:
            self.sharks[i].draw(screen, (100, 200, 0), p, 10)
        for i in self._n_plankton:
            self.plankton[i].draw()

        