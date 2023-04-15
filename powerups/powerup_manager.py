import random
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from powerups.powerup import DashPowerup, DoubleJumpPowerup, JumpPowerup, IncreaseAcceleration, IncreaseMaxSpeed, ShrinkPowerup, TeleportPowerup, TimeSlow, TimeStartsAt

import pygame
from timer import Timer


class PowerUpManager():
    def __init__(self, screen, player, timer):
        self.screen = screen
        self.possible_powerups = []
        self.current_powerups = []
        self.options_shown = 4
        self.selected = 0
        self.player = player
        self.level_timer = timer

    def add_tutorial_powerups(self):
        self.add_powerup(JumpPowerup("assets/powerups/jump.png", 3))
        self.add_powerup(DoubleJumpPowerup("assets/powerups/doubleJump.png"))
        self.add_powerup(TeleportPowerup("assets/powerups/teleport.png"))
        self.add_powerup(TimeSlow("assets/powerups/timeslow.png", 0.75))

        self.options = self.get_options()

    def add_level_powerups(self):
        self.add_powerup(JumpPowerup("assets/powerups/jump.png", 3))
        self.add_powerup(IncreaseAcceleration("assets/powerups/accel.png", 5))
        self.add_powerup(IncreaseMaxSpeed("assets/powerups/speed.png", 10))
        self.add_powerup(TimeSlow("assets/powerups/timeslow.png", 0.75))
        self.add_powerup(TimeStartsAt("assets/powerups/time.png", 5))
        self.add_powerup(DoubleJumpPowerup("assets/powerups/doubleJump.png"))
        self.add_powerup(DashPowerup("assets/powerups/dash.png"))
        self.add_powerup(TeleportPowerup("assets/powerups/teleport.png"))
        self.add_powerup(ShrinkPowerup("assets/powerups/shrink.png"))

        self.options = self.get_options()

    def add_powerup(self, powerup):
        self.possible_powerups.append(powerup)

    def infinitely_generate_powerups(self):
        self.add_powerup(JumpPowerup("assets/powerups/jump.png", 3))
        self.add_powerup(IncreaseAcceleration("assets/powerups/accel.png", 5))
        self.add_powerup(IncreaseMaxSpeed("assets/powerups/speed.png", 10))
        self.add_powerup(TimeSlow("assets/powerups/timeslow.png", 0.75))
        self.add_powerup(TimeStartsAt("assets/powerups/time.png", 5))

    def get_options(self):
        if len(self.possible_powerups) < self.options_shown:
            self.infinitely_generate_powerups()
        random.shuffle(self.possible_powerups)
        options = self.possible_powerups[:self.options_shown]
        self.possible_powerups = self.possible_powerups[self.options_shown:]
        return options

    def select(self):
        for i, option in enumerate(self.options):
            if (i == self.selected % self.options_shown):
                selected_option = option
            else:
                self.possible_powerups.append(option)
        self.options = self.get_options()
        return selected_option

    def render_image(self, image, x, y, width, height):
        image = pygame.image.load(image)
        image = pygame.transform.scale(image, (width, height))
        rect = image.get_rect()
        rect = rect.move((x, y))
        self.screen.blit(image, rect)

    def render_powerups(self):
        width = (SCREEN_HEIGHT/480) * 640

        space_between_powerups = 30
        p_width = (SCREEN_WIDTH - (self.options_shown+1) * space_between_powerups) / self.options_shown
        for i, powerup in enumerate(self.options):
            if i == self.selected % self.options_shown:
                self.render_image(powerup.image, i * (p_width + space_between_powerups) + space_between_powerups-10, 200-10, p_width+20, p_width+20)
            else:
                self.render_image(powerup.image, i * (p_width + space_between_powerups) + space_between_powerups, 200, p_width, p_width)

    def render_description(self):
        # render description and background rect
        font = pygame.font.SysFont("Segoe UI Black", 30)
        space_between_powerups = 30
        p_width = (SCREEN_WIDTH - (self.options_shown+1) * space_between_powerups) / self.options_shown
        pygame.draw.rect(self.screen, (255,255,255), (SCREEN_WIDTH*0.15, 200 + p_width + 50 - 20, SCREEN_WIDTH*0.7, 100))

        text = self.options[self.selected % self.options_shown].description
        lines = text.split("\n")
        for i, line in enumerate(lines):
            counting_text = font.render(line, 1, (0,0,0))
            counting_rect = counting_text.get_rect(center = (SCREEN_WIDTH/2, 200 + p_width + 50 + i * 30))
            self.screen.blit(counting_text, counting_rect)


    def render_timer(self, time):
        # render description
        font = pygame.font.SysFont("Segoe UI Black", 150)
        green = (52, 201, 59)
        red = (206, 54, 59)
        counting_text = font.render(f"{Timer.time_to_str(time)}", 1, green if time <= 10 else red)
        counting_rect = counting_text.get_rect(center = (SCREEN_WIDTH/2, 100))
        self.screen.blit(counting_text, counting_rect)

    def render_continue(self):
        # render description
        font = pygame.font.SysFont("Segoe UI Black", 30)
        counting_text = font.render("Press space to continue", 1, (0,0,0))
        counting_rect = counting_text.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 100))
        self.screen.blit(counting_text, counting_rect)