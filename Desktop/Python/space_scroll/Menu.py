from Start_up import*
from Upgrades import*
from Stars import Star, create_stars
from Settings import Settings

# generic class to hold a menu state
class GenericMenu(object):
    def __init__(self, own_state, title, options_list, select_length):
        self.own_state = own_state
        self.next_state = self.own_state
        self.title_surface = pygame.Surface((width, 150))
        self.select_surface = pygame.Surface((select_length, 30))
        self.title_surface.fill(main_theme)
        self.select_surface.fill(main_theme)
        self.title_surface.set_alpha(100)
        self.select_surface.set_alpha(100)
        self.star_list = create_stars("menu")
        self.list = options_list
        self.list_start = (50, 180)
        self.list_space = 30
        self.title = title
        self.title_pos = (50, 50)
        self.selected = 0
        self.go_to_selected = False

    def input(self, event_list):
        # alter selected based on key presses
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected -= 1
                if event.key == pygame.K_DOWN:
                    self.selected += 1

        self.check_selected()

    def check_selected(self):
        # check that selected does not go out of range
        if self.selected > len(self.list) - 1:
            self.selected = len(self.list) - 1
        elif self.selected < 0:
            self.selected = 0

    def remove_stars(self):
        # remove stars that are no longer colliding with the screen rect
        for x in range(0, len(self.star_list)):
            try:
                if not pygame.sprite.collide_rect(screen_rect, self.star_list[len(self.star_list) - x - 1]):
                    del self.star_list[len(self.star_list) - x - 1]
            except:
                # break in case [len(p_list) - x - 1] is out of range
                break

    def random_create_star(self):
        if random.randint(0, 2) == 1:
            # random speed of star just for variation
            r = random.choice([0.5, 1])
            # random to start on the right or bottom of screen with a bias
            # to starting on the bottom due to the shape of the screen
            if random.randint(0, 2):
                # start on bottom of screen
                s = Star(random.randint(0, width),   # x pos
                         height,                     # y pos
                         r,                          # dx
                         r)                          # dy
            else:
                # start on right of screen
                s = Star(width,                      # x pos
                         random.randint(0, height),  # y pos
                         r,                          # dx
                         r)                          # dy
            self.star_list.append(s)

    def update_stars(self):
        # call the update on all stars in star list
        for i in range(0, len(self.star_list)):
            self.star_list[i].update()

    def print_list(self):
        # print menu options and selected rect using the list spacing variables multiplied by iteration
        for x in range(0, len(self.list)):
            if x == self.selected:
                main_s.blit(self.select_surface, (0, self.list_start[1] + (self.list_space*x)))
                main_s.blit(menu_font.render(self.list[x], True, (255, 255, 255)), (self.list_start[0], self.list_start[1] + (self.list_space*x)))
            else:
                main_s.blit(menu_font.render(self.list[x], True, main_theme), (self.list_start[0], self.list_start[1] + (self.list_space*x)))

    def display_all(self):
        # fill the screen with darkness and display all elements of the menu
        main_s.fill((20, 20, 20))
        for i in range(0, len(self.star_list)):
            self.star_list[i].display()
        self.print_list()
        main_s.blit(self.title_surface, (0, 0))
        main_s.blit(title_font.render(str(self.title), True, (255, 255, 255)), self.title_pos)

    def run(self, event_list):
        # call all events needed for the menu to function
        # takes a list of key/mouse events and pass it to
        # the input function
        self.input(event_list)
        self.random_create_star()
        self.remove_stars()
        self.update_stars()
        self.display_all()

        # by default, next_state will be the objects own state
        # this can change in the derived classes input functions
        return self.next_state


class MainMenu(GenericMenu):
    def __init__(self):
        title = "Space Ships"
        list = ["Play", "Info", "Settings", "Quit"]
        select_length = 200
        own_state = home_state
        # call the super class and pass the main menu information
        super(MainMenu, self).__init__(own_state, title, list, select_length)

    def input(self, event_list):
        # supersede the input of the super class
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # set next state to the option selected
                    if self.selected == 0:
                        self.next_state = game_state
                    if self.selected == 1:
                        self.next_state = info_state
                    if self.selected == 2:
                        self.next_state = settings_state
                    if self.selected == 3:
                        self.next_state = quit_state
        super(MainMenu, self).input(event_list)


class InfoMenu(GenericMenu):
    def __init__(self):
        title = "Info"
        # no list or selected rect is needed for the info page
        list = []
        select_length = 0
        own_state = info_state
        super(InfoMenu, self).__init__(own_state, title, list, select_length)
        self.info_text = ["Destroy enemies, earn money and upgrade your ship!",
                          "",
                          "Arrow keys to move up and down",
                          "Space bar to shoot",
                          "ESC to pause and exit menu",
                          "",
                          "Created by Joe Pauley",
                          "September 2015"]

    def input(self, event_list):
        # supersede the input of the super class
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = home_state
        super(InfoMenu, self).input(event_list)

    def display_all(self):
        # supersede the display function (but call it and then display extra stuff)
        super(InfoMenu, self).display_all()
        for i in range(0, len(self.info_text)):
            main_s.blit(menu_font.render(self.info_text[i], True, main_theme), (self.list_start[0], self.list_start[1] + (i * 30)))


class InGameMain(GenericMenu):
    def __init__(self):
        title = "Paused"
        list = ["Shop", "Quit To Main"]
        select_length = 250
        own_state = pause_state
        # call the super class constructor passing the game menu information
        super(InGameMain, self).__init__(own_state, title, list, select_length)

    def input(self, event_list):
        # supersede the input function of the super class
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # set next state to the option selected
                    if self.selected == 0:
                        self.next_state = shop_state
                    elif self.selected == 1:
                        self.next_state = home_state
                if event.key == pygame.K_ESCAPE:
                    self.next_state = game_state
        super(InGameMain, self).input(event_list)

    def display_all(self):
        # supersede the display function (but call it and then display extra stuff)
        super(InGameMain, self).display_all()
        main_s.blit(font.render("ESC TO RETURN TO GAME", True, (255, 255, 255)), (width - 195, 5))


class Shop(GenericMenu):
    def __init__(self, player, health_bar):
        list = ["Speed", "Fire Rate", "Fire Power", "Coin Collection", "Restore 1 Health"]
        title = "Shop"
        rect_leng = width
        own_state = shop_state
        # call the super constructor passing the shop  information
        super(Shop, self).__init__(own_state, title, list, rect_leng)
        # create some extra object variables to hold palyer information and position
        self.player = player
        self.health_bar = health_bar
        self.upgrades_list_pos = (350, self.list_start[1])
        self.price_list_pos = (650, self.list_start[1])
        self.selected_info = ""

    def reset(self, player, health_bar):
        list = ["Speed", "Fire Rate", "Fire Power", "Coin Collection", "Restore 1 Health"]
        title = "Shop"
        rect_leng = width
        own_state = shop_state
        # call the super constructor passing the shop  information
        super(Shop, self).__init__(own_state, title, list, rect_leng)
        # create some extra object variables to hold palyer information and position
        self.player = player
        self.health_bar = health_bar
        self.upgrades_list_pos = (350, self.list_start[1])
        self.price_list_pos = (650, self.list_start[1])
        self.selected_info = ""

    def info_update(self):
        # update all information so that information is relevant when an upgrade is made
        self.player_info = [str(self.player.s_upgrade + 1) + " of " + str(len(upgrades_speed)),
                            str(self.player.g_s_upgrade + 1) + " of " + str(len(upgrades_gun_speed)),
                            str(self.player.g_p_upgrade + 1) + " of " + str(len(upgrades_gun_power)),
                            str(self.player.m_upgrade + 1) + " of " + str(len(upgrades_money_collection))]

        self.prices = [price_speed[self.player.s_upgrade],
                       price_gun_speed[self.player.g_s_upgrade],
                       price_gun_power[self.player.g_p_upgrade],
                       price_money_collection[self.player.m_upgrade]]

    def buy_upgrade(self):
        # checking what item is selected, check the user has
        # enough money for the upgrade and then check that
        # the user has not reached the max upgrade
        if self.selected == 0:
            if self.player.money >= self.prices[0]:
                if self.player.s_upgrade < len(price_speed):
                    self.player.money -= self.prices[0]
                    self.player.s_upgrade += 1
                    self.selected_info = "SPEED IMPROVED"
                else:
                    self.selected_info = "MAX LEVEL REACHED"
            else:
                self.selected_info = "YOU DO NOT HAVE ENOUGH COINS"
        elif self.selected == 1:
            if self.player.money >= self.prices[1]:
                if self.player.s_upgrade < len(price_gun_speed):
                    self.player.money -= self.prices[1]
                    self.player.g_s_upgrade += 1
                    self.selected_info = "GUN SPEED IMPROVED"
                else:
                    self.selected_info = "MAX LEVEL REACHED"
            else:
                self.selected_info = "YOU DO NOT HAVE ENOUGH COINS"
        elif self.selected == 2:
            if self.player.money >= self.prices[2]:
                if self.player.s_upgrade < len(price_gun_power):
                    self.player.money -= self.prices[2]
                    self.player.g_p_upgrade += 1
                    self.selected_info = "GUN POWER IMPROVED"
                else:
                    self.selected_info = "MAX LEVEL REACHED"
            else:
                self.selected_info = "YOU DO NOT HAVE ENOUGH COINS"
        elif self.selected == 3:
            if self.player.money >= self.prices[3]:
                if self.player.s_upgrade < len(price_money_collection):
                    self.player.money -= self.prices[3]
                    self.player.m_upgrade += 1
                    self.selected_info = "COIN COLLECTION IMPROVED"
                else:
                    self.selected_info = "MAX LEVEL REACHED"
            else:
                self.selected_info = "YOU DO NOT HAVE ENOUGH COINS"
        elif self.selected == 4:
            if self.player.money >= 30:
                if self.player.health < 10:
                    self.player.health += 1
                    self.player.health_update = True
                    self.player.money -= 30
                    self.selected_info = "SOME PLAYER HEALTH WAS RESTORED"
                else:
                    self.selected_info = "PLAYER HEALTH IS AT MAX"
            else:
                self.selected_info = "YOU DO NOT HAVE ENOUGH COINS"
        # update the players stats
        self.player.reload_upgrades()

    def input(self, event_list):
        # supersede the super class input function
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                # based on the selected option try to buy an upgrade
                self.selected_info = ""
                if event.key == pygame.K_RETURN:
                    self.buy_upgrade()
                if event.key == pygame.K_ESCAPE:
                    self.next_state = pause_state
        super(Shop, self).input(event_list)

    def print_shop_info(self):
        # display upgrade names, upgrade progress and upgrade prices
        for x in range(0, len(self.player_info)):
            if x == self.selected:
                main_s.blit(menu_font.render(self.player_info[x], True, (255, 255, 255)),
                            (self.upgrades_list_pos[0], self.upgrades_list_pos[1] + (self.list_space * x)))
                main_s.blit(menu_font.render(str(self.prices[x]), True, (255, 255, 255)),
                            (self.price_list_pos[0], self.price_list_pos[1] + (self.list_space * x)))
            else:
                main_s.blit(menu_font.render(self.player_info[x], True, main_theme),
                            (self.upgrades_list_pos[0], self.upgrades_list_pos[1] + (self.list_space * x)))
                main_s.blit(menu_font.render(str(self.prices[x]), True, main_theme),
                            (self.price_list_pos[0], self.price_list_pos[1] + (self.list_space * x)))

    def display_all(self):
        # supersede the display function (but call it and then display extra stuff)
        super(Shop, self).display_all()
        self.print_shop_info()
        main_s.blit(menu_font.render("COINS: " + str(self.player.money), True, (255, 255, 255)), (50, 100))
        main_s.blit(menu_font.render(self.selected_info, True, (0, 100, 100)), (50, 400))

    def run(self, event_list):
        self.info_update()
        # return the next state of the object (returned by the super class run function)
        return super(Shop, self).run(event_list)


class SettingsMenu(GenericMenu):
    def __init__(self):
        title = "Settings"
        options_list = ["Enemy Rate", "Enemy Health", "Particle Effects"]
        own_state = settings_state
        select_length = width
        super(SettingsMenu, self).__init__(own_state, title, options_list, select_length)
        self.changes_made = False
        self.selected_info = ""
        self.settings_list_pos = (650, self.list_start[1])
        self.settings_text = [str(settings.settings[0]) + " of " + str(len(settings.enemy_chance)),
                              str(settings.settings[1]) + " of " + str(len(settings.enemy_health_max)),
                              str(settings.settings[2]) + " of " + str(len(settings.enemy_particles))]

    def update_print_info(self):
        self.settings_text = [str(settings.settings[0]) + " of " + str(len(settings.enemy_chance)),
                              str(settings.settings[1]) + " of " + str(len(settings.enemy_health_max)),
                              str(settings.settings[2]) + " of " + str(len(settings.enemy_particles))]

    def print_settings(self):
        for i in range(0, len(self.settings_text)):
            if self.selected == i:
                main_s.blit(menu_font.render(self.settings_text[i], True, (255, 255, 255)),
                            (self.settings_list_pos[0], self.settings_list_pos[1] + (self.list_space * i)))
            else:
                main_s.blit(menu_font.render(self.settings_text[i], True, main_theme),
                            (self.settings_list_pos[0], self.settings_list_pos[1] + (self.list_space * i)))

    def input(self, event_list):
        # supersede the super class input function
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                self.selected_info = ""
                if event.key == pygame.K_ESCAPE:
                    self.next_state = home_state
                    # write the new settings to the settings file
                    # ready to be loaded the next time the user plays
                    settings.write_settings()

                if event.key == pygame.K_RIGHT:
                    # ensure the new list position is within the upper
                    # range of the list itself
                    if settings.settings[self.selected] + 1 < settings.list_lengths[self.selected] + 1:
                        settings.settings[self.selected] += 1
                        self.update_print_info()
                        settings.reload_settings()
                    else:
                        self.selected_info = "It can't get tougher!"

                if event.key == pygame.K_LEFT:
                    if settings.settings[self.selected] - 1 > 0:
                        settings.settings[self.selected] -= 1
                        self.update_print_info()
                        settings.reload_settings()
                    else:
                        self.selected_info = "It can't get easier!"
        super(SettingsMenu, self).input(event_list)

    def display_all(self):
        super(SettingsMenu, self).display_all()
        self.print_settings()
        main_s.blit(menu_font.render(self.selected_info, True, (0, 100, 100)), (50, 400))
        #print other menu stuff here


class GameOver(GenericMenu):
    def __init__(self):
        title = "Game Over!"
        options_list = ["Restart Game", "Quit To Main", "Quit Game"]
        own_state = game_over_state
        select_length = width
        super(GameOver, self).__init__(own_state, title, options_list, select_length)

    def input(self, event_list):
        # supersede the input of the super class
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # set next state to the option selected
                    if self.selected == 0:
                        self.next_state = reset_game_state
                    elif self.selected == 1:
                        self.next_state = home_state
                    elif self.selected == 2:
                        self.next_state = quit_state

        super(GameOver, self).input(event_list)
