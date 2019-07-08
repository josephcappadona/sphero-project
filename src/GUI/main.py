import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import r2d2
import server
import sys

keyboard_or_client = sys.argv[1] if len(sys.argv) > 1 else ''
if keyboard_or_client == 'keyboard':
    keyboard = True
    client = False
elif keyboard_or_client == 'client':
    client = True
    keyboard = False
else:
    print('USAGE:  python main.py keyboard|client\n')
    sys.exit(0)

pygame.init()
if client:
    serv = server.Server(None)
    serv.start()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

size = s_w, s_h = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('R2D2 GUI')

all_sprites_list = pygame.sprite.Group()

r2 = r2d2.R2D2()
r2.set_center_position(x=r2.rect.width/2, y=s_h-r2.rect.height/2)
if client:
    r2.set_socket_delegate(serv)

all_sprites_list.add(r2)

carry_on = True # continue until explicit exit
clock = pygame.time.Clock()

def keep_in_bounds(sprite):
    if sprite.my_x < 0:
        sprite.set_center_position(x=0)
    elif sprite.my_x > s_w:
        sprite.set_center_position(x=s_w)
    if sprite.my_y < 0:
        sprite.set_center_position(y=0)
    elif sprite.my_y > s_h:
        sprite.set_center_position(y=s_h)

while carry_on:

    # main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carry_on = False

    if keyboard:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            #r2.roll(1.0, -90, 0.25)
            pass
        if keys[pygame.K_RIGHT]:
            pass
            #r2.roll(1.0, 90, 0.25)
        if keys[pygame.K_UP]:
            r2.roll(1.0, 0, 0.05)
        if keys[pygame.K_DOWN]:
            r2.roll(1.0, 180, 0.05)
        if keys[pygame.K_r]:
            r2.rotate(3)
        if keys[pygame.K_l]:
            r2.rotate(-3)
        if keys[pygame.K_t]:
            r2.set_stance(1)
        if keys[pygame.K_b]:
            r2.set_stance(2)

    if client:
        r2.receive_and_handle_data()

    # game logic
    r2.update()
    keep_in_bounds(r2)
    all_sprites_list.update()

    # redraw code
    screen.fill(WHITE) # clear screen
    all_sprites_list.draw(screen)

    pygame.display.flip() # update the screen

    clock.tick(60)

pygame.quit()
