import math
from tiles import Wall, OpenTile

sin = lambda d: round(math.sin(d*math.pi/180.0), 2)
cos = lambda d: round(math.cos(d*math.pi/180.0), 2)

WHITE = (255, 255, 255)

def import_map_arr(filepath):
    with open(filepath, 'rt') as f:
        map_arr = f.read().strip().split('\n')
        return [row[::-1] for row in map_arr][::-1]

def convert_map_arr_to_sprites(map_arr, sprite_size=25):
    sprites = []
    for x, row in enumerate(map_arr):
        for y, char in enumerate(row):
            pos = (sprite_size*x, sprite_size*y)
            if char == ' ':
                sprite = OpenTile(pos, width=sprite_size, height=sprite_size)
            elif char == '$':
                sprite = OpenTile(pos, width=sprite_size, height=sprite_size, color=(0,255,0))
            elif char == '*':
                pass
            else:
                sprite = Wall(pos, width=sprite_size, height=sprite_size)
            sprites.append(sprite)
    return sprites

def keep_in_bounds(sprite, size):
    s_w, s_h = size
    if sprite.my_x < 0:
        sprite.set_center_position(x=0)
    elif sprite.my_x > s_w:
        sprite.set_center_position(x=s_w)
    if sprite.my_y < 0:
        sprite.set_center_position(y=0)
    elif sprite.my_y > s_h:
        sprite.set_center_position(y=s_h)

