from Start_up import*


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, count, cos_sin_none, bounce_range, dx, counter):
        self.surface = pygame.Surface((20, 20))
        self.rect = self.surface.get_rect()

        y_temp = pos[1]
        # None
        if cos_sin_none == 2:
            y_temp = random.randint(30, height - 30)
        # Sin
        if cos_sin_none == 1:
            if bounce_range <= 3:
                y_temp = random.randint(150, height - 170)
            if bounce_range > 3:
                y_temp = height/2
                if bounce_range > 3:
                    bounce_range = 3
        # Cos
        if cos_sin_none == 0 and bounce_range <= 4:
            y_temp = random.randint(100, height - 120)

        self.rect.x = pos[0]
        self.rect.y = y_temp

        self.cos_sin_none = cos_sin_none
        self.bounce_range = bounce_range

        self.cos_up = counter
        if self.cos_up:
            self.counter = 0
        else:
            if cos_sin_none == 0:
                self.counter = 180
            else:
                self.counter = 360
        self.dx = -dx
        self.dy = 0

        self.id = count
        self.health = random.randint(1, enemy_health_max)
        self.health_colours = [(50, 50, 50),      # low health
                               (100, 100, 100),
                               (200, 200, 200),
                               (255, 255, 255)]     # high health
        self.surface.fill(self.health_colours[self.health - 1])
        self.dead = False

        self.money = random.randint(5, 10)
        self.will_steal = self.money * 2

    def check_collide(self, bullet_list):
        for x in range(0, len(bullet_list)):
            if pygame.sprite.collide_rect(self, bullet_list[len(bullet_list) - x - 1]):
                self.health -= bullet_list[len(bullet_list) - x - 1].power
                if self.health > 0:
                    self.surface.fill(self.health_colours[self.health - 1])
                del bullet_list[len(bullet_list) - x - 1]

    def check_health(self):
        if self.health < 1:
            self.dead = True

    def move(self):
        if self.cos_up:
            self.counter += 2
        else:
            self.counter -= 2

        if self.counter >= 360:
            self.cos_up = False
        if self.counter <= 0:
            self.cos_up = True

        if self.cos_sin_none == 0:
            self.dy = int(math.cos(deg_to_rad(self.counter)) * self.bounce_range)
        elif self.cos_sin_none == 1:
            self.dy = int(math.sin(deg_to_rad(self.counter)) * self.bounce_range)
        elif self.cos_sin_none == 2:
            self.dy = 0

    def update(self, bullet_list):
        self.check_collide(bullet_list)
        self.check_health()
        self.move()
        self.rect.x += self.dx
        self.rect.y += self.dy

    def display(self):
        main_s.blit(self.surface, (self.rect.x, self.rect.y))
