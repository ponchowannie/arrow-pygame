import pygame
import sys
from components.constants import *
from core.button import Button  # Import Button from core/button.py
from components.constants import BROWN, LIGHT_BROWN

def show_start_screen(screen, background, clock):  # Add hat_image parameter
    start_button = Button(
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
    start_screen_active = True

    while start_screen_active:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            start_button.check_click(event)
            if event.type == pygame.MOUSEBUTTONDOWN and start_button._rect.collidepoint(event.pos):  # Use rect from Button
                start_screen_active = False

        start_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    
    easy_button = Button("Easy", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 100, 200, 60, lambda: None, 
        color=BROWN, hover_color=LIGHT_BROWN, font=pygame.font.Font("./components/fonts/western.ttf", 48))
    med_button = Button("Medium", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 30, 200, 60, lambda: None, 
        color=BROWN, hover_color=LIGHT_BROWN, font=pygame.font.Font("./components/fonts/western.ttf", 48))
    hard_button = Button("Hard", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 40, 200, 60, lambda: None, 
        color=BROWN, hover_color=LIGHT_BROWN, font=pygame.font.Font("./components/fonts/western.ttf", 48))
    diff_screen_active = True
    diff = 0
    while diff_screen_active:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button._rect.collidepoint(event.pos):
                    diff_screen_active = False
                    diff = 0
                if med_button._rect.collidepoint(event.pos):
                    diff_screen_active = False
                    diff = 1
                if hard_button._rect.collidepoint(event.pos):
                    diff_screen_active = False
                    diff = 2

        easy_button.draw(screen)
        med_button.draw(screen)
        hard_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    return diff

'''
import pygame
import sys
from components.constants import *

pygame.font.init()

BROWN = (165, 42, 42)
LIGHT_BROWN = (196, 164, 132)

try:
    FONT = pygame.font.Font("./components/fonts/western.ttf", 48)
except:
    FONT = pygame.font.Font(None, 48)

class Button:
    def __init__(self, text, x, y, width, height, callback, hat_image=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BROWN
        self.hover_color = LIGHT_BROWN
        self.callback = callback
        self.hat_image = hat_image
        self.start_sound = pygame.mixer.Sound("./components/sounds/game-start.mp3")

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, color, self.rect)
        text_surface = FONT.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        if self.hat_image:
            hat_rect = self.hat_image.get_rect()
            hat_rect.midbottom = (text_rect.left - 10, text_rect.top + 20)
            surface.blit(self.hat_image, hat_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.start_sound.play()
            self.callback()

def show_start_screen(screen, background, clock, hat_image):
    start_button = Button("Start Game", WINDOW_WIDTH//2 - 110, WINDOW_HEIGHT//2 - 35, 220, 70, lambda: None, hat_image=hat_image)
    start_screen_active = True

    while start_screen_active:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            start_button.check_click(event)
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.rect.collidepoint(event.pos):
                start_screen_active = False

        start_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
'''