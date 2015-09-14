from Start_up import*


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, power):
        self.surface = pygame.Surface((5, 2))
        self.surface.fill((200, 200, 200))
        self.rect = self.surface.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dx = 5

        self.power = power

    def update(self):
        self.rect.x += self.dx

    def display(self):
        main_s.blit(self.surface, (self.rect.x, self.rect.y))
