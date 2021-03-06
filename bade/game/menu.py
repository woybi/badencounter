import pygame
from pygame.locals import *

import consts as c


class Menu:
    def __init__(self, graphics, buttons_txt):
        self.graphics = graphics

        self.buttons = []

        self.title_font = pygame.font.Font("res/edosz.ttf", 110)
        self.title_text = "Bad Encounter"
        self.title_rendered = self.title_font.render(self.title_text, 1, (255, 50, 50))
        self.title_shadow = self.title_font.render(self.title_text, 1, (150, 50, 50))

        for i in range(0, len(buttons_txt), 1):
            self.buttons.append(Button(self.graphics, buttons_txt[i], c.WINDOW_WIDTH / 2, 300 + i * 100))

        self.background_img = pygame.transform.scale(self.graphics["menu_background.jpg"], (c.WINDOW_WIDTH, c.WINDOW_HEIGHT))

        self.clicked_button_txt = "NONE"


    def event(self, event):
        for button in self.buttons:
            button.event(event)
            if button.get_button_state() == "VALIDE":
                self.clicked_button_txt = button.get_button_txt()


    def update(self):
        for button in self.buttons:
            button.update()


    def draw(self):
        render = pygame.Surface((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))

        render.blit(self.background_img, (0, 0))
        render.blit(self.title_shadow, (c.WINDOW_WIDTH / 2 - self.title_shadow.get_width()/2 - 5, 250 / 2 - self.title_shadow.get_height()/2+5))
        render.blit(self.title_rendered, (c.WINDOW_WIDTH / 2 - self.title_rendered.get_width()/2, 250 / 2 - self.title_rendered.get_height()/2))

        for button in self.buttons:
            button.draw(render)

        return render


    def get_clicked_button_txt(self):
        return self.clicked_button_txt


    def set_clicked_button_to_blank(self):
        self.clicked_button_txt = ""


class Button:
    def __init__(self, graphics, caption, x, y):
        self.graphics = graphics

        self.caption = caption

        self.button_size = (500, 70)

        self.button_img = self.graphics["button_out.png"]
        self.button_rect = Rect((x - self.button_size[0] / 2, y -
                                 self.button_size[1] / 2),
                                (self.button_size[0], self.button_size[1]))

        self.button_state = "OUT"  # OUT, IN, CLICK

        self.font = pygame.font.Font("res/8bitwonder.ttf", 36)
        self.text = self.font.render(self.caption, 1, (10, 10, 10))
        self.text_rect = self.text.get_rect(center=(self.button_size[0] / 2 + self.button_rect[0], self.button_size[1] / 2 + self.button_rect[1]))


    def event(self, event):
        if event.type == MOUSEMOTION:
            if self.button_state != "CLICK":
                if self.button_rect.collidepoint(event.pos[0], event.pos[1]):
                    self.button_state = "IN"
                    self.button_img = self.graphics["button_in.png"]
                else:
                    self.button_state = "OUT"
                    self.button_img = self.graphics["button_out.png"]

        if event.type == MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos[0], event.pos[1]):
                self.button_state = "CLICK"
                self.button_img = self.graphics["button_click.png"]

        if event.type == MOUSEBUTTONUP:
            if self.button_rect.collidepoint(event.pos[0], event.pos[1]):
                self.button_img = self.graphics["button_in.png"]

                if self.button_state == "CLICK":
                    self.button_state = "VALIDE"
            else:
                self.button_state = "OUT"
                self.button_img = self.graphics["button_out.png"]


    def update(self):
        pass


    def draw(self, menu_render):
        menu_render.blit(pygame.transform.scale(self.button_img, self.button_size), self.button_rect)
        menu_render.blit(self.text, self.text_rect)


    def get_button_state(self):
        return self.button_state


    def get_button_txt(self):
        return self.caption
