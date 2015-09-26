from Start_up import*


class Particle(pygame.sprite.Sprite):
    def __init__(self, size, velocity, origin, colour):
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.Surface((size, size))
        if colour == (0, 100, 100):
            bright = random.randint(0, 50)
            self.surface.fill((50, 50 + bright, 50 + bright))
        else:
            bright = random.randint(0, 205)
            self.surface.fill((50 + bright, 50 + bright, 50 + bright))

        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = origin.center
        self.dx = velocity[0]
        self.dy = velocity[1]

    def update(self):
        # move the particle in the direction set
        self.rect.x += self.dx
        self.rect.y += self.dy

    def display(self):
        main_s.blit(self.surface, (self.rect.x, self.rect.y))
