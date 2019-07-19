import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from utils import sin, cos
from tiles import Wall

def handle_collisions(droid, all_sprites):
    col_dirs = set()
    for sprite in all_sprites:
        if isinstance(sprite, Wall):
            col_dirs.update(get_collision_directions(droid, sprite))

    if 'north' in col_dirs or 'south' in col_dirs:
        droid.block_vertical = True
    else:
        droid.block_vertical = False

    if 'east' in col_dirs or 'west' in col_dirs:
        droid.block_horizontal = True
    else:
        droid.block_horizontal = False

def is_south(droid, sprite):
    return sprite.rect.top < droid.rect.top

def is_north(droid, sprite):
    return sprite.rect.bottom > droid.rect.bottom

def is_west(droid, sprite):
    return sprite.rect.right > droid.rect.right

def is_east(droid, sprite):
    return sprite.rect.left < droid.rect.left

def is_moving_north(droid):
    return droid.speed > 0 and round(sin(-droid.heading + 90), 3) > 0

def is_moving_south(droid):
    return droid.speed > 0 and round(sin(-droid.heading + 90), 3) < 0

def is_moving_east(droid):
    return droid.speed > 0 and round(cos(-droid.heading + 90), 3) > 0

def is_moving_west(droid):
    return droid.speed > 0 and round(cos(-droid.heading + 90), 3) < 0

def is_horizontally_aligned(droid, sprite, thresh=10):
    return sprite.rect.left + thresh < droid.rect.left < sprite.rect.right - thresh or \
           sprite.rect.left + thresh < droid.rect.right < sprite.rect.right - thresh or \
           sprite.rect.left < droid.rect.centerx < sprite.rect.right

def is_vertically_aligned(droid, sprite, thresh=10):
    return sprite.rect.top + thresh < droid.rect.bottom < sprite.rect.bottom - thresh or \
           sprite.rect.top + thresh < droid.rect.top < sprite.rect.bottom - thresh or \
           sprite.rect.top < droid.rect.centery < sprite.rect.bottom

def get_collision_directions(droid, sprite):
    dirs = set()
    collision_point = pygame.sprite.collide_mask(droid, sprite)
    if collision_point:
        if is_south(droid, sprite) and is_moving_north(droid) and is_horizontally_aligned(droid, sprite):
            dirs.add('north')
        if is_north(droid, sprite) and is_moving_south(droid) and is_horizontally_aligned(droid, sprite):
            dirs.add('south')
        if is_west(droid, sprite) and is_moving_east(droid) and is_vertically_aligned(droid, sprite):
            dirs.add('east')
        if is_east(droid, sprite) and is_moving_west(droid) and is_vertically_aligned(droid, sprite):
            dirs.add('west')
    return dirs

