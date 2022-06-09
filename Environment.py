import numpy as np
from Flocking import flock_forces
import math
import resources.consts as consts
 
class Environment():

    def __init__(self, n_fishes, n_sharks, n_plankton,
                 fishes, sharks, plankton,
                 max_steps=100, 
                 canvas_shape=(1000, 500)):
        self._canvas_shape = canvas_shape
        self._n_fishes = n_fishes
        self._positions = 0
        self._n_sharks = n_sharks
        self._n_plankton = n_plankton
        self._fishes = fishes
        self._sharks = sharks
        self._plankton = plankton
        self._max_steps = max_steps

    def update_flocks(self, dt, positions, velocities):

        f1, f2, f3 = flock_forces(
            dt, positions, velocities
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

        positions = positions + velocities * dt * consts.FISH_SPEED
        return positions, velocities

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

    def update(self, dt):
        #TODO
        # collects observations and gives out actions

        #generic movement
        for i in self._n_fishes:
            # close2shark, agent = check_Proximity(self._fishes[i])
            # if close2shark: calculate_Velocity (self._fishes[i], agent)
            # With this new velocity the fish position is updated
            self._fishes[i].update(dt)
        for i in self._n_sharks:
            self._sharks[i].update(dt)

    # def draw(self, screen):
    #     #TODO
    #     # draws all agents on the screen
    #     for i in range(self.n_fishes):
    #         self.fishes[i].move()
    #         color = slef.fishes[i].energy_to_color()
    #         pg.draw.circle(screen, color, fish_positions[i], consts.FISH_SIZE)

        