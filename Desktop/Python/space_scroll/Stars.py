from Start_up import*

def create_stars(setting):
    star_list = []
    # star chance * 7 fills the screen with roughly the same amount of stars
    # as starts per update would give, star amount can be changed in startup.py
    for x in range(0, initial_stars):
        if setting == "game":
            # create stars moving from right to left
            s = Star(random.randint(0, width),   # x pos
                     random.randint(0, height),  # y pos
                     random.randint(1, 2),       # dx
                     0)                          # dy
        elif setting == "menu":
            # create slower stars moving diagonaly
            r = random.choice([0.5, 1])
            s = Star(random.randint(0, width),   # x pos
                     random.randint(0, height),  # y pos
                     r,                          # dx
                     r)                          # d
        star_list.append(s)
    return star_list

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        random_size = random.randint(1, 2)
        self.surface = pygame.Surface((random_size, random_size))
        self.surface.fill((150, 150, 150))
        self.rect = self.surface.get_rect()
        self.exact_x = x
        self.exact_y = y
        self.rect.x = x
        self.rect.y = y
        self.dx = -dx
        self.dy = -dy

    def update(self):
        # use of the exact position because rects can not hold float, if a
        # speed were a decimal it would not be added to the position correctly
        self.exact_x += self.dx
        self.exact_y += self.dy
        self.rect.x = self.exact_x
        self.rect.y = self.exact_y

    def display(self):
        main_s.blit(self.surface, (self.rect.x, self.rect.y))