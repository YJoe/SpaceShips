from Start_up import *


class NoteController:
    def __init__(self, start_pos):
        self.note_height = 30
        self.note_space = self.note_height + 10
        self.start_pos = start_pos
        self.note_list = []

    def add_note(self, text, colour):
        # create a new note and add it to the list of notes
        n = Notification(text, self.note_height, colour)
        self.note_list.append(n)

    def delete_oldest(self):
        # delete the first element of the list
        del self.note_list[0]

    def display(self):
        if show_notes:
            # display all notes in reverse order, hence the [len(notes) - 1 - n]
            for n in range(0, len(self.note_list)):
                self.note_list[len(self.note_list) - 1 - n].display((self.start_pos[0], self.start_pos[1] + (n * self.note_space)))

    def check_time(self):
        # only if there are notes in the list add to the counter
        # and check if the oldest card is out of time
        if len(self.note_list):
            if self.note_list[0].time < 1:
                self.delete_oldest()

    def update(self):
        self.check_time()
        for i in range(0, len(self.note_list)):
            self.note_list[i].update()


class Notification:
    def __init__(self, text, note_height, colour):
        self.text = text
        self.note_height = note_height
        # create a rect the same size as the string it holds
        # 10 being the rough size of a character in this font
        self.surface = pygame.Surface((10 * len(self.text), self.note_height))
        self.surface.fill(colour)
        self.surface.set_alpha(100)
        # create a deterioration time for the note (100 updates)
        self.time = 100

    def update(self):
        self.time -= 1

    def display(self, note_pos):
        # display the note rect and text
        text_pos_x, text_pos_y = note_pos
        text_pos_x += 5
        text_pos_y += 5
        main_s.blit(self.surface,
                    (note_pos[0] - len(self.text) * 10, note_pos[1]))
        main_s.blit(font.render(str(self.text), True, (255, 255, 255)),
                    (text_pos_x - len(self.text) * 10, text_pos_y))
