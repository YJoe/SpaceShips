from Start_up import*


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, power, shot_from):
        self.surface = pygame.Surface((5, 2))
        self.surface.fill((200, 200, 200))
        self.rect = self.surface.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        # the direction could just be controlled here but then
        # all bullets would damage anything, which I know is
        # more realistic but it would become too easy as enemies
        # could kill each other. maybe I'll add that as a setting
        # for the user to adjust if they want too.
        self.shot_from = shot_from
        if self.shot_from == "Player":
            self.dx = 5
        elif self.shot_from == "Enemy":
            self.dx = -5

        self.power = power

    def update(self):
        self.rect.x += self.dx

    def display(self):
        main_s.blit(self.surface, (self.rect.x, self.rect.y))
