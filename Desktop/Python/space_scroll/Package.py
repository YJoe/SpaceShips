from Start_up import*
from Upgrades import*


class Package(pygame.sprite.Sprite):
    def __init__(self, dx, pos):
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.dx = dx

    def update(self):
        # move the package towards the left of the screen
        self.rect.x += self.dx

    def display(self):
        main_s.blit(self.image, (self.rect.x, self.rect.y))


class EnemyDrop(Package):
    def __init__(self, dx, pos):
        super(EnemyDrop, self).__init__(dx, pos)
        # pick a random item excluding the last option in the list which is health
        self.holds = package_items[random.randint(0, len(package_items) - 2)]
        self.image.fill((0, 0, 150))


class HealthPack(Package):
    def __init__(self, dx, pos):
        super(HealthPack, self).__init__(dx, pos)
        # hold the item health
        self.holds = package_items[len(package_items) - 1]
        self.image.fill((0, 150, 0))


