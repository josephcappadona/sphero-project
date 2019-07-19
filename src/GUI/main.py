import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from sys import argv
from r2d2 import R2D2
#from wall import Wall
from server import Server
from utils import keep_in_bounds, WHITE, import_map_arr, convert_map_arr_to_sprites
from collisions import handle_collisions

SPRITE_SIZE = 25

if len(argv) > 2:
    print('USAGE:  python main.py [MAP.txt]')

map_filepath = argv[1] if len(argv) == 2 else None
map_arr = import_map_arr(map_filepath) if map_filepath else [[' ' for _ in range(20)] for _ in range(20)]

pygame.init()

server = Server(None)
server.start()

size = s_w, s_h = (SPRITE_SIZE*len(map_arr[0]), SPRITE_SIZE*len(map_arr))
screen = pygame.display.set_mode(size)

r2 = R2D2((SPRITE_SIZE, s_h-2*SPRITE_SIZE), width=SPRITE_SIZE, height=SPRITE_SIZE)
r2.set_socket_delegate(server)

map_sprites = convert_map_arr_to_sprites(map_arr, sprite_size=SPRITE_SIZE)
#wall_sprite = Wall((150, 150), width=SPRITE_SIZE, height=SPRITE_SIZE)

all_sprites_list = pygame.sprite.Group()
#all_sprites_list.add(wall_sprite)
for sprite in map_sprites:
    all_sprites_list.add(sprite)
all_sprites_list.add(r2)

playing = True
clock = pygame.time.Clock()

while playing:

    # main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    # handle client commands
    r2.receive_and_handle_data()

    # game logic
    handle_collisions(r2, all_sprites_list)
    r2.update()
    keep_in_bounds(r2, size)
    all_sprites_list.update()

    # redraw code
    screen.fill(WHITE) # clear screen
    all_sprites_list.draw(screen)

    pygame.display.flip() # update the screen
    clock.tick(60)

pygame.quit()
