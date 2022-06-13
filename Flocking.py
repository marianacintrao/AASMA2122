# File for the main flocking simulation for the boids
# Different sims can then use this to show real-time, debug, triangles etc.

import numpy as np



def flock_forces(pos, vel, map_size, influence_prox=0.5,
          alignment_factor = 0.1, cohesion_factor = 0.01,
          separation_factor = 0.05, speed=None):
    """
    Main algo for update boid positions and velocitie
    pos being the 2 x Number of boids array of x and y boid centers
    vel being the 2 x Number of boids array of x and y veolcites

    NOTE
    Rather than returning the posision and velocity of the boids, this
    func returns the forces acting on the boids.
    This func does not update the positions or velocities

    ALSO - speed variable not in use
    """

    # Bounce off walls...
    # Vel X:
    # vel[pos[:, 0]> map_size[0], 0] = -vel[pos[:, 0]> map_size[0], 0]
    # # Vel Y:
    # vel[pos[:, 1]> map_size[1], 1] = -vel[pos[:, 1]> map_size[1], 1]

    margin = 1
    pos[pos[:, 0]> map_size[0] + margin, 0] = 0 -margin
    pos[pos[:, 1]> map_size[1] + margin, 1] = 0 -margin
    pos[pos[:, 0]< 0 - margin, 0] = map_size[0] +margin
    pos[pos[:, 1]< 0 - margin, 1] = map_size[1] +margin

    # # # Pos X & Y:
    # pos[pos[:, 0] > map_size[0], 0] = map_size[0]
    # pos[pos[:, 1] > map_size[1], 1] = map_size[1]

    # # # Both miniums are 0 so this is easier:
    # # vel[pos < 0] = -vel[pos < 0]
    # # pos[pos < 0] = 0



    # Wrapping works nicely:
    # pos = pos % map_size

    # Get local boids:
    distance = np.linalg.norm(pos - pos[:,None], axis=-1)
    local = distance < influence_prox


    # # Cohesion:
    ##############
    # Add a veolcity vector towards the center of mass (COM):
    local_coms = (np.dot(local, pos).T / (local.sum(axis=1) + 1e-8)).T
    local_com_diff = local_coms - pos
    cohesion_force = (local_com_diff * cohesion_factor)

    #print("cohesion_force[0]: ", cohesion_force[0])

    # # Align:
    #############
    local_vel_avg = (np.dot(local, vel).T / (local.sum(axis=1) + 1e-8)).T
    local_vel_diff = local_vel_avg - vel
    align_force = (local_vel_diff * alignment_factor)

    # Drop Boids from their own local regions:
    np.fill_diagonal(local, False)
    # But ensure that they won't error out on a divide:
    np.fill_diagonal(distance, 1)

    #print("align_force[0]: ", align_force[0])

    # # Separation:
    ##############
    # There might be a better way to do this, but at the moment
    # I can't think of one...


    relative_x = pos[:, 0] - pos[:, 0, None]
    relative_y = pos[:, 1] - pos[:, 1, None]
    relative_x_local = relative_x.dot(local)
    relative_y_local = relative_y.dot(local)

    # Getting some errors when distance is 0... it seems highly unlikely
    # that the distance between boids as a float should ever be 0, but to
    # mitigate against it use small value here
    distance[distance == 0] = 1e-3

    test1 = relative_x_local / (distance**3)
    test2 = relative_y_local / (distance**3)
    
    #test1 = relative_x_local / (np.log(distance))
    #test2 = relative_y_local / (np.log(distance))
    # dividing by the distance converts to unit vectors, dividing again
    # adds a inverse component, stronger at close distances

    sep = -np.array([test1.sum(axis=1), test2.sum(axis=1)]).T
    sep_force = (sep * separation_factor)

    #print("sep_force[0]: ", sep_force[0])


    return cohesion_force, align_force, sep_force
