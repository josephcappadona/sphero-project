import contextlib
with contextlib.redirect_stdout(None):
    import pygame

class Wall(pygame.sprite.Sprite):
    
    def __init__(self, pos, width=50, height=50, color=(0,0,0)):
        super().__init__()
        x, y = pos

        self.image = pygame.Surface([width, height]).convert_alpha()
        self.image.fill((255,255,255))
        pygame.draw.rect(self.image, color, pygame.Rect((1,1), (width-1,height-1)))
        #pygame.draw.rect(self.image, color, pygame.Rect((0,0), (width,height)))

        self.rect = self.image.get_rect(x=x, y=y)
        self.mask = pygame.mask.from_surface(self.image)

class OpenTile(pygame.sprite.Sprite):
    
    def __init__(self, pos, width=50, height=50, color=(255,255,255)):
        super().__init__()
        x, y = pos

        self.image = pygame.Surface([width, height]).convert_alpha()
        self.image.fill((0,0,0,0))
        #pygame.draw.circle(self.image, (0,0,255), (50,50), 50)
        pygame.draw.rect(self.image, color, pygame.Rect((1,1), (width-1,height-1)))

        self.rect = self.image.get_rect(x=x, y=y)
        self.mask = pygame.mask.from_surface(self.image)

