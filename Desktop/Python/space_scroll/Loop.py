from Start_up import*
from Player import Player
from Menu import InGameMain, MainMenu, Shop, InfoMenu, SettingsMenu, GameOver
from Game import Game

# create all state objects
player = Player()
home = MainMenu()
info = InfoMenu()
game = Game(player)
paused = InGameMain()
shop = Shop(player)
settings = SettingsMenu()
game_over = GameOver()

def reset_next_states(to_reset):
    # reset all state objects so that "next_state"
    # is reverted to the object's own state
    for i in range(0, len(to_reset)):
        to_reset[i].next_state = to_reset[i].own_state

# set state to the home (main menu) state
state = home_state
running = True
while running:
    clock.tick(60)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                game.player.alive = False

    # control the game state
    # an object will always return its own state
    # number unless input events set otherwise
    if state == home_state:
        state = home.run(event_list)
        player.reset()
        game.reset(player)
        shop.reset(player)
    elif state == info_state:
        state = info.run(event_list)
    elif state == game_state:
        state = game.run(event_list)
    elif state == pause_state:
        state = paused.run(event_list)
    elif state == shop_state:
        state = shop.run(event_list)
    elif state == settings_state:
        state = settings.run(event_list)
    elif state == game_over_state:
        state = game_over.run(event_list)
    elif state == reset_game_state:
        player.reset()
        game.reset(player)
        shop.reset(player)
        state = game_state
    elif state == quit_state:
        running = False

    # ensure all "next_state" variables are set to the objects own state
    reset_next_states([home, info, game, paused, shop, settings, game_over])
    pygame.display.flip()

# exit all PyGame modules
pygame.quit()
