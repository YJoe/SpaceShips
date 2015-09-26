class Settings:
    def __init__(self):
        # the user can alter new_settings through the settings menu
        # writing to the settings file will only occur if the user
        # closes the settings function

        # create settings options
        self.enemy_chance = [300, 250, 200, 150, 100, 50, 10]
        self.enemy_health_max = [1, 2, 3, 4]
        self.enemy_particles = [0, 10, 30, 50, 70, 100, 200]
        self.default_options = [2, 2, 2]
        # It seems silly to have this list when I could just get
        # the lengths of each as I need them but it is handy to have
        # each length as an iterable list within the settings menu
        # input function as I need to compare the self.selected
        # variable with the length of the list to see if it is valid
        # this is also used a few lines below in the if self.read_settings
        self.list_lengths = []
        self.list_lengths.append(len(self.enemy_particles))
        self.list_lengths.append(len(self.enemy_health_max))
        self.list_lengths.append(len(self.enemy_particles))

        self.settings = []
        # keep track of where variables were read in case
        # new settings are needed to be written so that the
        # variables can be placed in the correct position
        self.variable_read_positions = []

        if self.read_settings():
            # settings have been stored in self.settings[]
            for i in range(0, len(self.settings)):
                # check the read settings are within their lists index
                if self.settings[i] > self.list_lengths[i] or self.settings[i] < 1:
                    # if not then load the default for that option
                    self.settings[i] = self.default_options[i]
                    print("ERROR: A setting was not loaded correctly, the default has been loaded")
                    print("for the setting in question, enter and exit the settings menu and the")
                    print("file values will be corrected, if not then the defaults will be loaded")
                    print("the next time you will play")
            print("Settings loaded successfully")
        else:
            # load all default list positions
            self.settings = self.default_options
            print("Settings did not load, all defaults loaded")

        # set the loaded values ready for use within the game
        self.loaded_enemy_chance = self.enemy_chance[self.settings[0] - 1]
        self.loaded_enemy_health_max = self.enemy_health_max[self.settings[1] - 1]
        self.loaded_enemy_particles = self.enemy_particles[self.settings[2] - 1]

    def reload_settings(self):
        # set the loaded values ready for use within the game
        self.loaded_enemy_chance = self.enemy_chance[self.settings[0] - 1]
        self.loaded_enemy_health_max = self.enemy_health_max[self.settings[1] - 1]
        self.loaded_enemy_particles = self.enemy_particles[self.settings[2] - 1]

    def read_settings(self):
        # read the settings file and store the variables
        line_count = 0
        try:
            file_r = open("Settings.txt", 'r')
            for line in file_r:
                if line[0] == "#":
                    pass
                else:
                    self.settings.append(int(line))
                    # recognise this as a position a setting was read
                    self.variable_read_positions.append(line_count)
                line_count += 1

        except StandardError:
            # there were issues with reading the file
            # return an empty list and False so that
            # the settings class will load defaults
            return False

        file_r.close()
        return True

    def write_settings(self):
        file_r = open("Settings.txt", 'r')
        all_lines = file_r.readlines()
        file_r.seek(0)
        # this variable is used so that the "old settings"
        # can be removed allowing me to easily delete the
        # 0 index position each time in the bellow for loop
        all_settings = [] + self.settings
        setting_lines = [] + self.variable_read_positions
        line_count = 0
        for line in file_r:
            if line_count == setting_lines[0]:
                all_lines[line_count] = str(all_settings[0]) + "\n"
                del all_settings[0]
                del setting_lines[0]
            line_count += 1

        with open('Settings.txt', 'w') as file_w:
            file_w.writelines(all_lines)
