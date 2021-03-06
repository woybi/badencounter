import os

import pygame
from pygame.locals import *

import consts as c
from game.level import Level
from game.menu import Menu
from game.mob.bobby import Bobby
from game.dialog import Dialog

class MainGame(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((c.WINDOW_WIDTH,
                                               c.WINDOW_HEIGHT))

        self.clock = pygame.time.Clock()

        self.graphics = {}
        self.__load_graphics()


    def main_loop(self):
        print("entering main_loop")

        state = "MENU" # MENU, GAME, HOWTOPLAY, CREDITS, EXIT

        while state != "EXIT":
            if state == "MENU":
                state = self.__menu()

            if state == "GAME":
                state = self.__game()

            if state == "HOWTOPLAY":
                state = self.__how_to_play()

            if state == "CREDITS":
                state = self.__credits()

        print("exiting main_loop")


    def __menu(self):
        print("entering __menu")

        menu = Menu(self.graphics, ("play", "how to play", "exit"))

        state_to_return = "EXIT"
        goon = True
        while goon:
            # events
            for event in pygame.event.get():
                if event.type == QUIT:
                    goon = False

                menu.event(event)

            # updates
            menu.update()

            choice = menu.get_clicked_button_txt()

            if choice == "play":
                state_to_return = "GAME"
                goon = False

            if choice == "how to play":
                state_to_return = "HOWTOPLAY"
                goon = False

            #if choice == "credits":
            #    state_to_return = "CREDITS"
            #    goon = False

            if choice == "exit":
                state_to_return = "EXIT"
                goon = False

            # draws
            finalrender = pygame.Surface((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))

            finalrender.blit(menu.draw(), (0, 0))

            self.screen.blit(pygame.transform.scale(finalrender,
                                                    (c.WINDOW_WIDTH,
                                                     c.WINDOW_HEIGHT)),
                             (0, 0))

            pygame.display.flip()

            self.clock.tick(30)

        print("exiting __menu")

        return state_to_return


    def __game(self):
        print("entering __game")

        levels = Level(self.graphics, "home")

        bobby = Bobby(self.graphics)

        finalrender = pygame.Surface((levels.get_map_size()[0],
                                      levels.get_map_size()[1]))

        in_dial = False
        pnj_name = "null"
        dial_count = 1

        state_to_return = "EXIT"
        goon = True
        while goon:
            #print(self.clock.get_fps())
            deltatime = self.clock.tick(30) / 100.0

            #events
            for event in pygame.event.get():
                if event.type == QUIT:
                    goon = False

                if in_dial:
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_ESCAPE:
                            in_dial = False
                            pnj_name = "null"
                            dial_count = 1

                        if event.key == pygame.K_RETURN:
                            dial_count += 1
                            if dial_count > len(levels.chars[pnj_name]["dials"]):
                                in_dial = False
                                pnj_name = "null"
                                dial_count = 1
                else:
                    levels.event(event)

                    bobby.event(event)

            # updates
            bob_value = bobby.update(deltatime, levels.get_map_size(), levels)

            if bobby.get_state_to_return() == "MENU":
                state_to_return = "MENU"
                goon = False

            levels.update(bob_value, bobby)

            if levels.currentmap == "credits":
                goon = False
                state_to_return = "CREDITS"
                break

            if finalrender.get_width() != levels.get_map_size()[0] or finalrender.get_height() != levels.get_map_size()[1]:
                finalrender = pygame.Surface((levels.get_map_size()[0],
                                              levels.get_map_size()[1]))

            # draws
            finalrender.blit(levels.draw(), (0, 0))

            b_x, b_y = bobby.get_pos()
            finalrender.blit(bobby.draw(), (b_x, b_y))

            self.screen.blit(pygame.transform.scale(finalrender,
                                                    (c.WINDOW_WIDTH,
                                                     c.WINDOW_HEIGHT)),
                             (0, 0))

            if bob_value.split(' ')[0] == "pnj" and not in_dial: # or in_dial
                in_dial = True
                pnj_name = bob_value.split(' ')[1]

            elif in_dial:
                bobby_talk = False

                my_font = pygame.font.Font("res/ubuntumono-r.ttf", 22)
                my_string = levels.chars[pnj_name]["dials"][str(dial_count)]
                if my_string[0] == "*":
                    bobby_talk = True
                    my_string = "<Bobby>  " + my_string[1:]
                else:
                    my_string = "<" + pnj_name[0].upper() + pnj_name[1:] + ">  " + my_string

                my_rect = pygame.Rect((0, 0, c.WINDOW_WIDTH, c.WINDOW_HEIGHT/4))
                rendered_text = Dialog().render_textrect(my_string, my_font, my_rect, (216, 216, 216), (0, 0, 20, 225), 0)
                self.screen.blit(rendered_text, (0, c.WINDOW_HEIGHT - rendered_text.get_height()))

                # TODO: Change head if ":" or "*"
                if bobby_talk:
                    head = pygame.transform.scale(self.graphics["bobby_head.png"], (175, rendered_text.get_height()+50))
                else:
                    head = pygame.transform.scale(self.graphics[pnj_name + "_head.png"], (175, rendered_text.get_height()+50))

                self.screen.blit(head, (0, c.WINDOW_HEIGHT - rendered_text.get_height()))

                continue_font = my_font
                continue_font.set_italic(True)
                dial_left = "(" + str(dial_count) + "/" + str(len(levels.chars[pnj_name]["dials"])) + ")"
                continue_font_rendered = continue_font.render("Press Enter to continue... " + dial_left, 1, (150, 150, 150))
                self.screen.blit(continue_font_rendered, (c.WINDOW_WIDTH-continue_font_rendered.get_width(), c.WINDOW_HEIGHT - continue_font_rendered.get_height()))

            pygame.display.flip()

        print("exiting __game")

        return state_to_return


    def __how_to_play(self):
        print("entering __how_to_play")

        background = pygame.transform.scale(self.graphics["credits_background.jpg"], (c.WINDOW_WIDTH, c.WINDOW_HEIGHT))

        font = pygame.font.Font("res/ubuntumono-r.ttf", 22)
        text = \
            ["HOW TO PLAY", \
             "", \
             "In this game, you will play the role of \"Bobby\" wich is a young man that is,", \
             "discovering the world.", \
             "You will be able to move with the four directionnal arrows of your", \
             "keyboard (up, down, left and right).", \
             "Bobby begin his journey at home, you will need to talk to your mother,", \
             "and then move to the next level.", \
             "To talk to other people, just move to them with the directionnal arrows of", \
             "your keyboard and then press Enter to go through the dialog.", \
             "In each level, there will be a man or a woman. You will have to talk with each", \
             "of them before moving to the next level, in order to discover interesting", \
             "informations about sects.", \
             "There will be a road drawn with dirt and gravel which will guide to the", \
             "the differents levels. Be careful, before getting to the next level,", \
             "don't forget to talk with the people you will encounter!", \
             "If you don't find any people on a level, just follow the dirt path to get to", \
             "the next level.", \
             "", \
             "Enjoy !"]

        font_continue = pygame.font.Font("res/ubuntumono-r.ttf", 22)
        rendered_text_continue = font_continue.render("Click or press Escape or Enter to get back to the menu ...", 1, (150, 150, 150))

        state_to_return = "EXIT"
        goon = True
        while goon:
            # events
            for event in pygame.event.get():
                if event.type == QUIT:
                    goon = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        state_to_return = "MENU"
                        goon = False

                if event.type == pygame.MOUSEBUTTONUP:
                    state_to_return = "MENU"
                    goon = False

            # updates

            # draws
            finalrender = pygame.Surface((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))

            finalrender.blit(background, (0, 0))

            line_posy = 0
            for line in text:
                rendered_text = font.render(line, 1, (240, 190, 255))
                finalrender.blit(rendered_text, (c.WINDOW_WIDTH/2 - rendered_text.get_width()/2, 100 - rendered_text.get_height() + line_posy))
                line_posy += font.size(line)[1] + 5

            finalrender.blit(rendered_text_continue, (c.WINDOW_WIDTH/2 - rendered_text_continue.get_width()/2, c.WINDOW_HEIGHT - rendered_text_continue.get_height()-10))

            self.screen.blit(pygame.transform.scale(finalrender,
                                                    (c.WINDOW_WIDTH,
                                                     c.WINDOW_HEIGHT)),
                             (0, 0))

            pygame.display.flip()

            self.clock.tick(30)

        print("exiting __how_to_play")

        return state_to_return

    def __credits(self):
        print("entering __credits")

        background = pygame.transform.scale(self.graphics["credits_background.jpg"], (c.WINDOW_WIDTH, c.WINDOW_HEIGHT))

        font = pygame.font.Font("res/ubuntumono-r.ttf", 50)
        text = \
            ["Thanks for Playing !", \
             "", \
             "CREDITS :", \
             "", \
             "Programming : Eyal CHOJNOWSKI", \
             "Drawing : Maréva SEI and Alycia MOLLE"]

        font_continue = pygame.font.Font("res/ubuntumono-r.ttf", 22)
        rendered_text_continue = font_continue.render("Click or press Escape or Enter to get back to the menu ...", 1, (150, 150, 150))

        state_to_return = "EXIT"
        goon = True
        while goon:
            # events
            for event in pygame.event.get():
                if event.type == QUIT:
                    goon = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        state_to_return = "MENU"
                        goon = False

                if event.type == pygame.MOUSEBUTTONUP:
                    state_to_return = "MENU"
                    goon = False

            # updates

            # draws
            finalrender = pygame.Surface((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))

            finalrender.blit(background, (0, 0))

            line_posy = 0
            for line in text:
                rendered_text = font.render(line, 1, (200, 150, 255))
                finalrender.blit(rendered_text, (c.WINDOW_WIDTH/2 - rendered_text.get_width()/2, 230 - rendered_text.get_height() + line_posy))
                line_posy += font.size(line)[1] + 5

            finalrender.blit(rendered_text_continue, (c.WINDOW_WIDTH/2 - rendered_text_continue.get_width()/2, c.WINDOW_HEIGHT - rendered_text_continue.get_height()-10))

            self.screen.blit(pygame.transform.scale(finalrender,
                                                    (c.WINDOW_WIDTH,
                                                     c.WINDOW_HEIGHT)),
                             (0, 0))

            pygame.display.flip()

            self.clock.tick(30)

        print("exiting __credits")

        return state_to_return


    def __load_graphics(self):
        for subdir, dirs, files in os.walk("res"):
            for item in files:
                if item.lower().endswith('.png') or item.lower().endswith('.jpg'):
                    try:
                        self.graphics[item] = pygame.image.load(str(subdir) + "/" +
                                                                str(item)).convert_alpha()
                    except Exception as ex:
                        print("caught exception at __load_graphics():", ex)

