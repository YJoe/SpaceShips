from Start_up import *
from Bullet import Bullet
from Upgrades import*

class HealthBar:
    def __init__(self, player):
        self.x = 100
        self.y = 10
        self.player = player
        self.bar = pygame.Surface((20 * self.player.health, 10))
        self.bar.fill((0, 255, 0))

        self.bar_back = pygame.Surface((21 * self.player.health, 20))
        self.bar_back.fill((50, 50, 50))

    def reset(self, player):
        self.player = player
        self.bar = pygame.Surface((20 * self.player.health, 10))
        self.bar.fill((0, 255, 0))

    def update_health(self):
        print("update")
        self.bar = pygame.Surface((20 * self.player.health, 10))
        self.bar.fill((0, 255, 0))

    def display(self):
        main_s.blit(self.bar_back, (self.x - 5, self.y - 5))
        main_s.blit(self.bar, (self.x, self.y))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.surface = pygame.Surface((20, 20))
        self.surface.fill(main_theme)
        self.rect = self.surface.get_rect()
        self.rect.x = 10
        self.rect.y = height/2
        self.dy = 0
        self.cool = True
        self.cool_counter = 0
        self.bullets_used = 0
        self.money = 0
        self.health = 10
        self.alive = True
        self.hit = False
        self.health_update = False

        self.s_upgrade = 0
        self.m_upgrade = 0
        self.g_s_upgrade = 0
        self.g_p_upgrade = 0

        self.speed = upgrades_speed[self.s_upgrade]
        self.money_collection = upgrades_money_collection[self.m_upgrade]
        self.cool_time = upgrades_gun_speed[self.g_s_upgrade]
        self.bullet_power = upgrades_gun_power[self.g_p_upgrade]

    def reset(self):
        self.surface = pygame.Surface((20, 20))
        self.surface.fill(main_theme)
        self.rect = self.surface.get_rect()
        self.rect.x = 10
        self.rect.y = height/2
        self.dy = 0
        self.cool = True
        self.cool_counter = 0
        self.bullets_used = 0
        self.money = 0
        self.health = 10
        self.alive = True

        self.s_upgrade = 0
        self.m_upgrade = 0
        self.g_s_upgrade = 0
        self.g_p_upgrade = 0

        self.speed = upgrades_speed[self.s_upgrade]
        self.money_collection = upgrades_money_collection[self.m_upgrade]
        self.cool_time = upgrades_gun_speed[self.g_s_upgrade]
        self.bullet_power = upgrades_gun_power[self.g_p_upgrade]

    def reload_upgrades(self):
        # set all player variables to the relevant upgrades
        self.speed = upgrades_speed[self.s_upgrade]
        self.money_collection = upgrades_money_collection[self.m_upgrade]
        self.cool_time = upgrades_gun_speed[self.g_s_upgrade]
        self.bullet_power = upgrades_gun_power[self.g_p_upgrade]

    def get_coins(self, coins):
        # multiply all coins by the money collection upgrade
        self.money += coins * self.money_collection

    def check_collide(self, bullet_list):
        self.hit = False
        # check the enemy against all off the bullets in the bullet list
        for x in range(0, len(bullet_list)):
            # check that the bullet was shot from a
            # player and should damage the enemy
            if bullet_list[len(bullet_list) - x - 1].shot_from == "Enemy":
                if pygame.sprite.collide_rect(self, bullet_list[len(bullet_list) - x - 1]):
                    # if a bullet has collided remove the correct amount of health based
                    # off of the power of the players bullets
                    self.health -= 1
                    self.hit = True
                    if self.health == 0:
                        self.alive = False
                    # if the enemy will still be alive set its new colour based off of
                    # its new health value
                    # remove the bullet
                    del bullet_list[len(bullet_list) - x - 1]

    def shoot(self, bullet_list):
        # check the gun can shoot
        if self.cool:
            # create a new bullet and add it to the games bullet list
            new_bullet = Bullet(self.rect.center, self.bullet_power, "Player")
            bullet_list.append(new_bullet)
            # set the gun to not able to shoot
            self.cool = False
            self.bullets_used += 1
        return bullet_list

    def move(self, direction):
        # move the player by a direction (1 or -1) and speed
        self.dy = direction * self.speed

    def check_cool_down(self):
        # allow the gun to run or add to the cool counter
        if not self.cool:
            self.cool_counter += 1
            if self.cool_counter > self.cool_time:
                self.cool = True
                self.cool_counter = 0

    def collect_package(self, item, note_controller, health_bar):
        # determine the package picked up:
        # SU = Speed Upgrade
        # GSU = Gun Speed Upgrade
        # GPU = Gun Power Upgrade
        # MCU = Money Collection Upgrade
        # M = Money
        # H = Health
        # then check that the player does not have the max amount of upgrades
        # if no then add the upgrade and reload the player stats
        # create relevant notes to display
        if item == "SU":
            if self.s_upgrade < len(upgrades_speed) - 1:
                self.s_upgrade += 1
                note_controller.add_note("Speed + 1", main_theme)
            else:
                note_controller.add_note("Speed is maxed", main_theme)
        elif item == "GSU":
            if self.g_s_upgrade < len(upgrades_gun_speed) - 1:
                self.g_s_upgrade += 1
                note_controller.add_note("Gun speed + 1", main_theme)
            else:
                note_controller.add_note("Gun speed is maxed", main_theme)
        elif item == "GPU":
            if self.g_p_upgrade < len(price_gun_power) - 1:
                self.g_p_upgrade += 1
                note_controller.add_note("Gun power + 1", main_theme)
            else:
                note_controller.add_note("Gun power is maxed", main_theme)
        elif item == "MCU":
            if self.m_upgrade < len(upgrades_money_collection) - 1:
                note_controller.add_note("Money collection + 1", main_theme)
                self.m_upgrade += 1
            else:
                note_controller.add_note("Money collection is maxed", main_theme)
        elif item == "M":
            random_amount = random.randint(10, 50)
            note_controller.add_note("+ " + str(random_amount * self.money_collection) + " coins", main_theme)
            self.money += random_amount
        elif item == "H":
            if self.health < 10:
                self.health += 1
                note_controller.add_note("1 health point restored", main_theme)
                health_bar.update_health ()

            else:
                note_controller.add_note("Health is at max", main_theme)

        self.reload_upgrades()

    def check_package_collide(self, package_list, note_controller, health_bar):
        # check if a package collides with the player and remove it from the package_list
        for i in range(0, len(package_list)):
            if pygame.sprite.collide_rect(self, package_list[len(package_list) - i - 1]):
                self.collect_package(package_list[len(package_list) - i - 1].holds, note_controller, health_bar)
                del package_list[len(package_list) - i - 1]

    def update(self, package_list, note_controller, bullet_list, health_bar):
        # update the player object
        self.check_package_collide(package_list, note_controller, health_bar)
        self.check_cool_down()
        self.check_collide(bullet_list)
        if self.money < 0:
            self.money = 0
        self.rect.y += self.dy
        self.dy = 0

    def display(self):
        main_s.blit(self.surface, (self.rect.x, self.rect.y))

