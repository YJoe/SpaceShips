from Start_up import*
from Bullet import Bullet


class Enemy(pygame.sprite.Sprite):
    # class to hold an enemy taking the random variables given in the game class
    def __init__(self, id):
        self.surface = pygame.Surface((20, 20))
        self.rect = self.surface.get_rect()

        self.pos = (width, height/2)
        self.move_function = random.randint(0, 2)
        self.bounce_range = random.randint(2, 7)
        self.cool = True
        self.cool_time = random.randint(30, 70)
        self.cool_counter = 0
        self.bullet_power = 1

        # random.randint(1, 2))
        # create a temporary variable for the y coordinate
        y_temp = self.pos[1]
        # if statements to determine the movement of the enemy cos = 0, sin = 1, none = 2
        # the y position will then be randomised such that its function will not take it 
        # off the screen
        if self.move_function == 2:  # Move in a straight line
            y_temp = random.randint(30, height - 30)
        elif self.move_function == 1:  # Move using a sin function
            if self.bounce_range <= 3:
                y_temp = random.randint(150, height - 170)
            if self.bounce_range > 3:
                y_temp = height/2
                if self.bounce_range > 3:
                    self.bounce_range = 3
        elif self.move_function == 0 and self.bounce_range <= 4:  # Move using a sin function
            y_temp = random.randint(100, height - 120)

        # set the positions to the rect
        self.rect.x = self.pos[0]
        self.rect.y = y_temp

        # used to start either moving upwards or downwards
        self.function_up = random
        # set the counter accordingly
        if self.function_up:
            self.counter = 0
        else:
            if self.move_function == 0:
                self.counter = 180
            else:
                self.counter = 360
    
        self.dx = -random.randint(1, 3)
        self.dy = 0

        # give the enemy an id so that it can be removed from lists
        # easily in the kill enemy function in the Game class
        self.id = id

        # set the health of the enemy and give it a shade based on that
        self.health = random.randint(1, settings.loaded_enemy_health_max)
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
            # check that the bullet was shot from a
            # player and should damage the enemy
            if bullet_list[len(bullet_list) - x - 1].shot_from == "Player":
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

    def shoot(self, bullet_list):
        # check the gun can shoot
        if self.cool:
            # create a new bullet and add it to the games bullet list
            new_bullet = Bullet(self.rect.center, self.bullet_power, "Enemy")
            bullet_list.append(new_bullet)
            # set the gun to not able to shoot
            self.cool = False
        return bullet_list

    def check_cool_down(self):
        # allow the gun to run or add to the cool counter
        if not self.cool:
            self.cool_counter += 1
            if self.cool_counter > self.cool_time:
                self.cool = True
                self.cool_counter = 0
                # create a new cool down time, this makes the
                # enemies shooting a little more unpredictable
                self.cool_time = random.randint(40, 300)

    def move(self):
        # if the player should be moving up add 2 to its counter
        # else subtract 2 from the counter
        if self.function_up:
            self.counter += 2
        else:
            self.counter -= 2

        # if the counter has reached the top, set the player to
        # move downwards and if the counter is too low, set the
        # player to move upwards
        if self.counter >= 360:
            self.function_up = False
        if self.counter <= 0:
            self.function_up = True

        # check the function of the enemy and calculate its new y speed
        # the enemy will not move in an actual sin wave but the behaviour is
        # much more interesting i think
        if self.move_function == 0:
            self.dy = int(math.cos(deg_to_rad(self.counter)) * self.bounce_range)
        elif self.move_function == 1:
            self.dy = int(math.sin(deg_to_rad(self.counter)) * self.bounce_range)
        elif self.move_function == 2:
            self.dy = 0

    def update(self, bullet_list):
        # call all of the functions needed to update the enemy
        # passing the bullet list to the collide function
        self.check_collide(bullet_list)
        self.check_health()
        self.move()
        # check if the gun can shoot
        # then try to shoot the gun
        self.check_cool_down()
        self.shoot(bullet_list)

        # set the new position 
        self.rect.x += self.dx
        self.rect.y += self.dy

    def display(self):
        # display the surface at the rect's coordinates
        main_s.blit(self.surface, (self.rect.x, self.rect.y))
