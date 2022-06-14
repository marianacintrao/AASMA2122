from colour import Color

FISH_MAX_ENERGY = 100
SCALE_FACTOR = 50
influence_prox = 2.5
  
red = Color("red")
green = Color("green")
FISH_COLORS = list(red.range_to(green, FISH_MAX_ENERGY))

SHARK_SPEED = 2
FISH_SPEED = 0.5

PLANKTON_SIZE = 4
FISH_SIZE = 10
SHARK_SIZE = 40

PLANKTON_REPRODUCTION_RATE = 1
PLANKTON_REPRODUCTION_RADIUS = 1

FISH_REPRODUCTION_RATE = 0.2
FISH_REPRODUCTION_RADIUS = 1
FISH_INTENTIONS = 6
FISH_GO_TO_PLANKTON, FISH_EAT, ESCAPE, FISH_REPRODUCE, FLOCK, FISH_DIE = range(FISH_INTENTIONS)


def energy_to_color(energy: int) -> tuple:
    color = FISH_COLORS[energy - 1]
    hex = color.hex_l
    # Pass 16 to the integer function for change of base
    return tuple([int(hex[i:i+2], 16) for i in range(1,6,2)])