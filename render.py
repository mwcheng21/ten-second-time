


from constants import COLS, SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from player import Player
from timer import Timer
import pygame

from utils import resource_path
SCROLL_THRESH = 200

class Renderer():
    def __init__(self, screen):
        self.screen = screen
        self.shift = 0
        self.LEFT_BAR = SCREEN_WIDTH * 0.25
        self.RIGHT_BAR = SCREEN_WIDTH * 0.75
        self.current_shift = 0
        self.counter = 0

    def render_image(self, image, x, y, width=None, height=None, flipped=False, shift=True):
        image = pygame.image.load(image)
        if not (width is None and height is None):
            image = pygame.transform.scale(image, (width, height))
        rect = image.get_rect()

        if shift:
            rect = rect.move((x + self.current_shift, y))
        else:
            rect = rect.move((x, y))
        image = pygame.transform.flip(image, True, False) if flipped else image
        self.screen.blit(image, rect)
        return image, rect

    def render_background(self, cur_starting_x: int = 0):
        self.screen.fill((0,0,0))
        images = ["set3_tiles"] * 1
        width = (SCREEN_HEIGHT/480) * 640
        x = -self.current_shift
        for image in images:
            self.render_image(resource_path(f"assets/background/set3_background.png"), x, 0, width, SCREEN_HEIGHT)
            self.render_image(resource_path(f"assets/background/{image}.png"), x, 0, width, SCREEN_HEIGHT)
            x += width

    def render_world(self, world_map, player, help_manager):
        for tile in world_map.tiles:
            coords = tile[1]
            self.screen.blit(tile[0], (coords.x + self.current_shift, coords.y))

        if player.help_index != -1:
            # render help text in top right
            font = pygame.font.SysFont("Segoe UI Black", 22)
            black = (0, 0, 0)
            for i, helpSign in enumerate(world_map.help_list):
                if helpSign.idx == player.help_index:
                    pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(SCREEN_WIDTH/2 - 200, 20, 400, 150))
                    sign_description = help_manager.descriptions[i]
                    lines = sign_description.split("\n")
                    for i, line in enumerate(lines):
                        self.render_text(line, SCREEN_WIDTH/2, 50 + i * 30, font, black, centered=True)
                    break

        

    def render_player(self, player: Player, cur_starting_x: int = 0):
        assert self.current_shift <= 0
        if (player.x < self.LEFT_BAR + abs(self.current_shift)):
            self.move_left((self.LEFT_BAR + abs(self.current_shift)) - player.x)
        elif (player.x > self.RIGHT_BAR + abs(self.current_shift)):
            self.move_right(player.x - (self.RIGHT_BAR + abs(self.current_shift)))

        walking = ["walk2", "walk2", "walk6",  "walk6", "walk2", "walk2","walk7", "walk7"]
        standing = ["stand"]
        jumping = ["up4"]
        if player.isJumping:
            image_name = jumping[self.counter % len(jumping)]
        elif player.isWalking:
            image_name = walking[self.counter % len(walking)]
        else:
            image_name = standing[0]

        image, _ = self.render_image(resource_path(f"assets/player/Player Blue/playerBlue_{image_name}.png"), player.x, player.y, player.width, player.height, flipped=(not player.isMovingRight))

    def render_timer(self, running_time: float, font):
        counting_string = Timer.time_to_str(running_time)
        green = (52, 201, 59)
        red = (206, 54, 59)
        counting_text = font.render(str(counting_string), 1, green if running_time < 10 else red)

        #render in top left corner
        counting_rect = counting_text.get_rect(center = (0 + counting_text.get_width() /2, 0 + counting_text.get_height() / 2))

        # render background
        pygame.draw.rect(self.screen, (0,0,0), counting_rect)

        self.screen.blit(counting_text, counting_rect)

    def render_update(self):
        if abs(self.shift - self.current_shift) > 0:
            self.current_shift += (self.shift - self.current_shift)/2

    def move_left(self, amount):
        self.shift += amount
        if self.shift > 0:
            self.shift = 0

    def move_right(self, amount):
        self.shift -= amount
        if self.shift < -TILE_SIZE * COLS + SCREEN_WIDTH:
            self.shift = -TILE_SIZE * COLS + SCREEN_WIDTH

    def reset(self):
        self.shift = 0
        self.current_shift = 0

    def update(self):
        self.counter += 1

    def render_main_menu(self):
        self.screen.fill((0,0,0))
        self.render_image(resource_path("assets/background/set3_background.png"), 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, shift=False)
        self.render_image(resource_path("assets/background/set3_hills.png"), 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, shift=False)

        # Render logo at center of screen
        pygame.logo = pygame.image.load("assets/logo.png")
        logo_rect = pygame.logo.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))
        self.screen.blit(pygame.logo, logo_rect)
        
        
        # Render start, settings, and quit buttons (size 190 by 49)
        button_width = 190
        button_height = 49
        _, tutorial_button = self.render_image(resource_path("assets/buttons/tutorial_button.png"), SCREEN_WIDTH/2 - button_width/2, logo_rect.y + logo_rect.height, shift=False)
        _, start_button = self.render_image(resource_path("assets/buttons/start_button.png"), SCREEN_WIDTH/2 - button_width/2, logo_rect.y + logo_rect.height + button_height + 10, shift=False)
        _, quit_button = self.render_image(resource_path("assets/buttons/quit_button.png"), SCREEN_WIDTH/2 - button_width/2, logo_rect.y + logo_rect.height + 2 * (button_height + 10), shift=False)

        return start_button, tutorial_button, quit_button
    
    def render_text(self, text, x, y, font, color, centered = False):
        text = font.render(text, 1, color)
        if centered:
            text_rect = text.get_rect(center = (x, y))
            self.screen.blit(text, text_rect)
        else:
            self.screen.blit(text, (x, y))

    def render_stats(self, level_time, total_time, player):
        font = pygame.font.SysFont("Segoe UI Black", 30)
        black = (0,0,0)

        # Render background
        self.render_image(resource_path("assets/background/set3_background.png"), 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, shift=False)
        self.render_image(resource_path("assets/background/set3_tiles.png"), 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, shift=False)

        # Render logo at center of screen
        multiplyer = 0.6
        self.render_image(resource_path("assets/logo.png"), 50, 0, 550*multiplyer, 310*multiplyer, shift=False)
        self.render_text(Timer.time_to_str(level_time), 550*multiplyer + 50, 25, pygame.font.SysFont("Segoe UI Black", 100), (52, 201, 59))

        col1x = SCREEN_WIDTH/2 - 250
        col2x = SCREEN_WIDTH/2 + 100

        true_button = resource_path("assets/buttons/blue_boxCheckmark.png")
        false_button = resource_path("assets/buttons/blue_boxCross.png")
        # Render level time
        self.render_text("Level Time:", col1x, SCREEN_HEIGHT/2 - 150, font, black)
        self.render_text(Timer.time_to_str(level_time), col2x, SCREEN_HEIGHT/2 - 150, font, black)

        # Render total time
        self.render_text("Total Time:", col1x, SCREEN_HEIGHT/2 - 100, font, black)
        self.render_text(Timer.time_to_str(total_time), col2x, SCREEN_HEIGHT/2 - 100, font, black)

        # Render times completed
        self.render_text("Completions:", col1x, SCREEN_HEIGHT/2 - 50, font, black)
        self.render_text(str(player.completions), col2x, SCREEN_HEIGHT/2 - 50, font, black)

        # Render deaths
        self.render_text("Deaths:", col1x, SCREEN_HEIGHT/2, font, black)
        self.render_text(str(player.deaths), col2x, SCREEN_HEIGHT/2, font, black)
        
        # render if teleporter is on
        self.render_text("Teleport On:", col1x, SCREEN_HEIGHT/2 + 50, font, black)
        self.render_image(true_button if player.canTeleport else false_button, col2x, SCREEN_HEIGHT/2 + 50, 20, 20, shift=False)
        
        # render if double jump is on
        self.render_text("Double Jump On:", col1x, SCREEN_HEIGHT / 2 + 100, font, black)
        self.render_image(true_button if player.canDoubleJump else false_button, col2x, SCREEN_HEIGHT/2 + 100, 20, 20, shift=False)

        # render if can dash
        self.render_text("Dash On:", col1x, SCREEN_HEIGHT / 2 + 150, font, black)
        self.render_image(true_button if player.canDash else false_button, col2x, SCREEN_HEIGHT/2 + 150, 20, 20, shift=False)

        # Render continue button
        _, continue_button = self.render_image(resource_path("assets/buttons/continue_button.png"), SCREEN_WIDTH/2 - 190/2, SCREEN_HEIGHT/2 + 200, shift=False)

        return continue_button