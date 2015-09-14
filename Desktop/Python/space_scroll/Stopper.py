from Start_up import*


class Stopper(pygame.sprite.Sprite):
    def __init__(self, pos, kill_e, kill_b):
        # kill_e = Kill enemies (True or false)
        # kill_b = Kill bullets
        self.surface = pygame.Surface((10, height))
        self.rect = self.surface.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.kill_e = kill_e
        self.kill_b = kill_b
        self.enemies_collided = 0

    def collide(self, bullets, enemies, ship, note_controller):
        if self.kill_b:
            # if the stopper is meant to remove bullets
            # if it collides with a bullet
            # remove it from the list
            for x in range(0, len(bullets)):
                if pygame.sprite.collide_rect(self, bullets[len(bullets) - x - 1]):
                    del bullets[len(bullets) - x - 1]

        if self.kill_e:
            # if the stopper is meant to remove enemies
            # if it collides with a enemy
            # remove it from the list
            # give the player money and create a note to display
            for y in range(0, len(enemies)):
                if pygame.sprite.collide_rect(self, enemies[len(enemies) - y - 1]):
                    ship.money -= enemies[len(enemies) - y - 1].will_steal
                    note_controller.add_note("- " + str(enemies[len(enemies) - y - 1].will_steal) + " coins", (100, 0, 0))
                    del enemies[len(enemies) - y - 1]
                    self.enemies_collided += 1

    def update(self, bullets, enemies, ship, note_controller):
        self.collide(bullets, enemies, ship, note_controller)
