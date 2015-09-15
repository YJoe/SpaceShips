from Start_up import*


class Enemy(pygame.sprite.Sprite):
    # class to hold an enemy taking the random variables given in the game class
    # I realise I could create the variables here and pass nothing, in fact that's
    # probably the next thing i will change
    def __init__(self, pos, count, cos_sin_none, bounce_range, dx, counter):
        self.surface = pygame.Surface((20, 20))
        self.rect = self.surface.get_rect()

        # create a temporary variable for the y coordinate
        y_temp = pos[1]
        # if statements to determine the movement of the enemy cos = 0, sin = 1, none = 2
        # the y position will then be randomised such that its function will not take it 
        # off the screen 
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

        # set the positions to the rect
        self.rect.x = pos[0]
        self.rect.y = y_temp

        self.cos_sin_none = cos_sin_none
        self.bounce_range = bounce_range

        # used to start either moving upwards or downwards
        self.cos_up = counter
        # set the counter accordingly
        if self.cos_up:
            self.counter = 0
        else:
            if cos_sin_none == 0:
                self.counter = 180
            else:
                self.counter = 360
    
        self.dx = -dx
        self.dy = 0

        # give the enemy an id so that it can be removed from lists
        # easily in the kill enemy function in the Game class
        self.id = count
        # set the health of the enemy and give it a shade based on that
        self.health = random.randint(1, enemy_health_max)
        self.health_colours = [(50, 50, 50),      # low health
                               (100, 100, 100),
                               (200, 200, 200),
                               (255, 255, 255)]     # high health
        self.surface.fill(self.health_colours[self.health - 1])
        self.dead = False

        # how much money will the player get for killing the enemy
        self.money = random.randint(5, 10)
        # the enemy will steal twice the amount if it reaches the left side
        self.will_steal = self.money * 2

    def check_collide(self, bullet_list):
        # check the enemy against all off the bullets in the bullet list
        for x in range(0, len(bullet_list)):
            if pygame.sprite.collide_rect(self, bullet_list[len(bullet_list) - x - 1]):
                # if a bullet has collided remove the correct amount of health based
                # off of the power of the players bullets
                self.health -= bullet_list[len(bullet_list) - x - 1].power
                # if the enemy will still be alive set its new colour based off of
                # its new health value
                if self.health > 0:
                    self.surface.fill(self.health_colours[self.health - 1])
                # remove the bullet 
                del bullet_list[len(bullet_list) - x - 1]

    def check_health(self):
        # function to check if the enemy is dead
        if self.health < 1:
            self.dead = True

    def move(self):
        # if the player should be moving up add 2 to its counter
        # else subtract 2 from the counter
        if self.cos_up:
            self.counter += 2
        else:
            self.counter -= 2

        # if the counter has reached the top, set the player to
        # move downwards and if the counter is too low, set the
        # player to move upwards
        if self.counter >= 360:
            self.cos_up = False
        if self.counter <= 0:
            self.cos_up = True

        # check the funcion of the enemy and calculate its new y speed
        # the enemy will not move in an actual sin wave but the behaviour is
        # much more interesting i think
        if self.cos_sin_none == 0:
            self.dy = int(math.cos(deg_to_rad(self.counter)) * self.bounce_range)
        elif self.cos_sin_none == 1:
            self.dy = int(math.sin(deg_to_rad(self.counter)) * self.bounce_range)
        elif self.cos_sin_none == 2:
            self.dy = 0

    def update(self, bullet_list):
        # call all of the functions needed to update the enemy
        # passing the bullet list to the collide function
        self.check_collide(bullet_list)
        self.check_health()
        self.move()
        # set the new position 
        self.rect.x += self.dx
        self.rect.y += self.dy

    def display(self):
        # display the surface at the rect's coordinates
        main_s.blit(self.surface, (self.rect.x, self.rect.y))
