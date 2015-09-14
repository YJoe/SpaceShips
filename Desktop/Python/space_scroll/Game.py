from Start_up import*
from Player import Player
from Bullet import Bullet
from Enemy import Enemy
from Stopper import Stopper
from Particle import Particle
from Stars import Star, create_stars
from Package import Package
from Notes import NoteController


class Game:
    def __init__(self, play):
        self.own_state = game_state
        self.next_state = self.own_state
        self.player = play
        self.enemy_id_tracker = 0
        self.left_stop = Stopper((-30, 0), True, False)
        self.right_stop = Stopper((width, 0), False, True)
        self.bullet_list = []
        self.enemy_list = []
        self.kill_list = []
        self.particle_list = []
        self.package_list = []
        self.to_update = []
        self.to_display = []
        self.to_text = []
        self.star_list = create_stars("game")
        self.info_bar = pygame.Surface((width, 30))
        self.info_bar.fill(main_theme)
        self.info_bar.set_alpha(100)
        self.note_controller = NoteController((width - 10, 40))

    def update_all(self):
        # a check for all update elements, providing the
        # relevant information for the objects update
        for x in range(0, len(self.to_update)):
            if isinstance(self.to_update[x], Particle):
                self.to_update[x].update()
            elif isinstance(self.to_update[x], Star):
                self.to_update[x].update()
            elif isinstance(self.to_update[x], Enemy):
                self.to_update[x].update(self.bullet_list)
            elif isinstance(self.to_update[x], Player):
                self.to_update[x].update(self.package_list, self.note_controller)
            elif isinstance(self.to_update[x], Bullet):
                self.to_update[x].update()
            elif isinstance(self.to_update[x], Package):
                self.to_update[x].update()
            elif isinstance(self.to_update[x], NoteController):
                self.to_update[x].update()
            elif isinstance(self.to_update[x], Stopper):
                self.to_update[x].update(self.bullet_list, self.enemy_list, self.player, self.note_controller)

    def display_all(self):
        # fill screen with black and display all game information
        main_s.fill((20, 20, 20))
        for x in range(0, len(self.to_display)):
            self.to_display[x].display()
        main_s.blit(self.info_bar, (0, 0))
        main_s.blit(font.render("ESC TO PAUSE", True, (255, 255, 255)), (width - 115, 5))

    def text_all(self):
        # display all text needed at the top of the screen
        total_length = 0
        for x in range(0, len(self.to_text)):
            main_s.blit(font.render(str(self.to_text[x]), True, (255, 255, 255)), (5 + (15 * total_length), 5))
            total_length += len(self.to_text[x])

    def hit_particles(self, rect_hit):
        # create particles with random speeds, directions and sizes
        to_create = particle_count
        numbers_z = range(-10, 10)
        numbers_nz = range(-10, -1) + range(1, 10)
        for x in range(0, to_create):
            x_temp = random.choice(numbers_z)
            y_temp = random.choice(numbers_z)

            dy = y_temp
            dx = x_temp
            # make sure that dx and dy are not both 0 so that there
            # are no particles static on the screen
            if x_temp == 0 and y_temp != 0:
                dy = y_temp
                dx = x_temp
            if y_temp == 0 and x_temp != 0:
                dy = y_temp
                dx = x_temp
            if x_temp == y_temp == 0:
                dy = random.choice(numbers_nz)
                dx = random.choice(numbers_nz)

            particle = Particle(random.randint(1, 3), (dx, dy), rect_hit)
            self.particle_list.append(particle)

    def remove_particles(self):
        # remove particles that are no longer colliding with the screen
        # removed from the end first so that the list does not effect
        # later elements to remove
        for x in range(0, len(self.particle_list)):
            try:
                if not pygame.sprite.collide_rect(screen_rect, self.particle_list[len(self.particle_list) - x - 1]):
                    del self.particle_list[len(self.particle_list) - x - 1]
            except:
                # break in case [len(p_list) - x - 1] is out of range
                break

    def remove_stars(self):
        # remove stars that are no longer colliding with the screen
        # removed from the end first so that the list does not effect
        # later elements to remove
        for x in range(0, len(self.star_list)):
            try:
                if not pygame.sprite.collide_rect(screen_rect, self.star_list[len(self.star_list) - x - 1]):
                    del self.star_list[len(self.star_list) - x - 1]
            except:
                # break in case [len(p_list) - x - 1] is out of range
                break

    def check_enemy_alive(self):
        # add enemies to a removal list if they are dead
        for x in range(0, len(self.enemy_list)):
            if self.enemy_list[x].dead:
                self.kill_list.append(self.enemy_list[x])

    def kill_enemies(self):
        # remove enemies from enemy list that are on the kill list
        # create a package and give the player the coins dropped
        # create particles originating from the now dead enemy
        # create a notification for the user saying they have found money
        for x in range(0, len(self.kill_list)):
            for y in range(0, len(self.enemy_list)):
                try:
                    if self.kill_list[len(self.kill_list) - x - 1].id == self.enemy_list[len(self.enemy_list) - y - 1].id:
                        del self.kill_list[len(self.kill_list) - x - 1]
                        self.note_controller.add_note("+ " + str(self.enemy_list[len(self.enemy_list) - y - 1].money * self.player.money_collection) + " coins", main_theme)
                        self.player.get_coins(self.enemy_list[len(self.enemy_list) - y - 1].money)
                        self.hit_particles(self.enemy_list[len(self.enemy_list) - y - 1].rect)
                        self.random_event_package(self.enemy_list[len(self.enemy_list) - y - 1].dx,
                                                  self.enemy_list[len(self.enemy_list) - y - 1].rect.center)
                        del self.enemy_list[len(self.enemy_list) - y - 1]
                        break
                except:
                    break

    def random_event_enemy(self):
        # create an enemy if the random variable is 1
        if random.randint(1, enemy_chance) == 1:
            enemy = Enemy((width, height/2), self.enemy_id_tracker, random.randint(0, 2), random.randint(2, 7), random.randint(1, 2), random.randint(0, 1))
            self.enemy_list.append(enemy)
            self.enemy_id_tracker += 1

    def random_event_star(self):
        if random.randint(1, star_chance) == 1:
            # create a star starting at the right and set to move to the left
            s = Star(width + 10,                 # x pos (start a little off screen)
                     random.randint(0, height),  # y pos
                     random.randint(1, 2),       # dx
                     0)                          # dy
            self.star_list.append(s)

    def random_event_package(self, speed, pos):
        # random chance that package will be created
        if random.randint(1, package_change) == 1:
            p = Package(speed, pos)
            self.package_list.append(p)

    def input(self, event_list):
        # player input
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.player.move(-1)
        if key[pygame.K_DOWN]:
            self.player.move(1)
        if key[pygame.K_SPACE]:
            self.bullet_list = self.player.shoot(self.bullet_list)

        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = pause_state

    def run(self, event_list):
        # run all game functions
        self.input(event_list)
        self.random_event_enemy()
        self.random_event_star()
        self.check_enemy_alive()
        self.kill_enemies()
        self.remove_particles()
        self.remove_stars()
        # reload all lists
        self.to_display = self.package_list + self.star_list + self.bullet_list + self.enemy_list + \
                          self.particle_list + [self.player, self.note_controller]
        self.to_update = [self.player, self.note_controller, self.left_stop, self.right_stop] + self.package_list + self.star_list + \
                          self.bullet_list + self.enemy_list + self.particle_list
        self.to_text = [str(self.player.money) + " COINS",
                        str(self.player.bullets_used) + " BULLETS USED",
                        str(self.left_stop.enemies_collided) + " ENEMIES PASSED"]

        self.update_all()
        self.display_all()
        self.text_all()

        # by default return the games own state value
        # otherwise this will be changed in the user input
        return self.next_state
