import pygame
import sys
from components.constants import *
from core.button import Button  # Import Button from core/button.py
from components.constants import BROWN, LIGHT_BROWN

class StartScreen(Button):
    def __init__(self, screen, background, clock):
        self.screen = screen
        self.background = background
        self.clock = clock
        self.start_button = Button(
            "Start Game", 
            WINDOW_WIDTH // 2 - 100, 
            WINDOW_HEIGHT // 2 - 40, 
            200, 
            80, 
            lambda: None, 
            color=BROWN,
            hover_color=LIGHT_BROWN,
            font=pygame.font.Font("./components/fonts/western.ttf", 48),
            isHat=True,
        )
        self.easy_button = Button(
            "Easy", 
            WINDOW_WIDTH // 2 - 100, 
            WINDOW_HEIGHT // 2 - 100, 
            200, 
            60, 
            lambda: None, 
            color=BROWN, 
            hover_color=LIGHT_BROWN, 
            font=pygame.font.Font("./components/fonts/western.ttf", 48)
        )
        self.med_button = Button(
            "Medium", 
            WINDOW_WIDTH // 2 - 100, 
            WINDOW_HEIGHT // 2 - 30, 
            200, 
            60, 
            lambda: None, 
            color=BROWN, 
            hover_color=LIGHT_BROWN, 
            font=pygame.font.Font("./components/fonts/western.ttf", 48)
        )
        self.hard_button = Button(
            "Hard", 
            WINDOW_WIDTH // 2 - 100, 
            WINDOW_HEIGHT // 2 + 40, 
            200, 
            60, 
            lambda: None, 
            color=BROWN, 
            hover_color=LIGHT_BROWN, 
            font=pygame.font.Font("./components/fonts/western.ttf", 48)
        )

    def run(self):
        diff = self._show_start_screen()
        return diff

    def _show_start_screen(self):
        start_screen_active = True
        while start_screen_active:
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.start_button.check_click(event)
                if event.type == pygame.MOUSEBUTTONDOWN and self.start_button._rect.collidepoint(event.pos):
                    start_screen_active = False

            self.start_button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)
        
        return self._show_difficulty_screen()

    def _show_difficulty_screen(self):
        diff_screen_active = True
        diff = 0
        while diff_screen_active:
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.easy_button._rect.collidepoint(event.pos):
                        diff_screen_active = False
                        diff = 0
                    if self.med_button._rect.collidepoint(event.pos):
                        diff_screen_active = False
                        diff = 1
                    if self.hard_button._rect.collidepoint(event.pos):
                        diff_screen_active = False
                        diff = 2

            self.easy_button.draw(self.screen)
            self.med_button.draw(self.screen)
            self.hard_button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)
        return diff