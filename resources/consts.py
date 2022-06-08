from colour import Color


FISH_MAX_ENERGY = 1000
  
red = Color("red")
green = Color("green")
FISH_COLORS = list(red.range_to(green, FISH_MAX_ENERGY))

SHARK_SPEED = 2
FISH_SPEED = 1

FISH_SIZE = 5
SHARK_SIZE = 30

def energy_to_color(energy: int) -> tuple:
    color = FISH_COLORS[energy-1]
    hex = color.hex_l
    # Pass 16 to the integer function for change of base
    return tuple([int(hex[i:i+2], 16) for i in range(1,6,2)])
