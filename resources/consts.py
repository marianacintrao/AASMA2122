from colour import Color

visualize = False


FISH_MAX_ENERGY = 100
SHARK_MAX_ENERGY = 200
SCALE_FACTOR = 50
influence_prox = 2.5

map_size = [20, 15]

margin = 0.5
  
red = Color("red")
green = Color("green")
blue = Color("blue")
FISH_COLORS = list(red.range_to(green, FISH_MAX_ENERGY))
SHARK_COLORS = list(red.range_to(blue, SHARK_MAX_ENERGY))

SHARK_SPEED = 0.006
FISH_SPEED = 0.004

PLANKTON_SIZE = 4
FISH_SIZE = 10
SHARK_SIZE = 40

PLANKTON_REPRODUCTION_RATE = .5
PLANKTON_REPRODUCTION_RADIUS = 1

FISH_REPRODUCTION_RATE = 0.001
FISH_REPRODUCTION_RADIUS = .5
FISH_INTENTIONS = 6
FISH_GO_TO_PLANKTON, FISH_EAT, ESCAPE, FISH_REPRODUCE, FLOCK, FISH_DIE = range(FISH_INTENTIONS)

FISH_THRESHOLD_FOR_HUNGER = .7
FISH_ENERGY_FOR_REPRODUCING = .7
FISH_ENERGY_SPENT_REPRODUCING = .02
FISH_RADIUS_FOR_REPRODUCING = .05
FISH_RADIUS_FOR_EATING = .05

FISH_NUTRITIONAL_VALUE = FISH_MAX_ENERGY

SHARK_VISION_RADIUS = 4
SHARK_SCARED_OF_N_FISHES = 10
SHARK_REPRODUCTION_RATE = 0.001
SHARK_REPRODUCTION_RADIUS = .5
SHARK_ENERGY_FOR_REPRODUCING = .7
# SHARK_THRESHOLD_FOR_HUNGER = .7
SHARK_RATIO_FOR_REPRODUCING = .05
SHARK_RADIUS_FOR_EATING = .2

SHARK_INTENTIONS = 5
SHARK_GO_TO_FISH, SHARK_EAT, SHARK_REPRODUCE, SHARK_DIE, SHARK_MOVE = range(SHARK_INTENTIONS)

def fish_energy_to_color(energy: int) -> tuple:
    color = FISH_COLORS[energy - 1]
    hex = color.hex_l
    # Pass 16 to the integer function for change of base
    return tuple([int(hex[i:i+2], 16) for i in range(1,6,2)])


def shark_energy_to_color(energy: int) -> tuple:
    color = SHARK_COLORS[energy - 1]
    hex = color.hex_l
    # Pass 16 to the integer function for change of base
    return tuple([int(hex[i:i+2], 16) for i in range(1,6,2)])