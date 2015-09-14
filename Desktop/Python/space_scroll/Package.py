from Start_up import*
from Upgrades import*


class Package(pygame.sprite.Sprite):
    def __init__(self, dx, pos):
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 70, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.dx = dx
        self.holds = package_items[random.randint(0, len(package_items) - 1)]

    def update(self):
        # move the package towards the left of the screen
        self.rect.x += self.dx

    def display(self):
        main_s.blit(self.image, (self.rect.x, self.rect.y))
