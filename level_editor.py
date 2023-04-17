from genericpath import isfile
import json
from os import listdir
import pygame
import os
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, GameState, ROWS, COLS
from utils import resource_path

import time

class Level():
    def __init__(self, level_name='custom_level'):
        creation_time = time.time()
        # convert time to MM/DD_HH:MM:SS
        creation_time = time.strftime('%m_%d_%H_%M_%S', time.localtime(creation_time))
        self.csv = resource_path(f'assets/levels/{level_name}{creation_time}.csv')
        self.json = resource_path(f'assets/levels/{level_name}{creation_time}.json')
        self.name = level_name

        # create the files
        with open(self.csv, 'w') as f:
            row = '-1,' * (COLS-1) + '-1\n'
            f.writelines(row * ROWS)

        with open(self.json, 'w') as f:
            f.write(f'{{"playerx": 9, "playery": 12}}')

    def write_to_csv(self, x, y, tile_type):
        with open(self.csv, 'r') as f_in:
            lines = f_in.readlines()
            with open(self.csv, 'w') as f_out:
                line = lines[y].strip().split(',')
                line[x] = str(tile_type)
                lines[y] = ','.join(line) + "\n"
                f_out.writelines(lines)

    def set_player(self, x, y):
        with open(self.json, 'w') as f:
            f.write(f'{{"playerx": {x}, "playery": {y}}}')

class LevelEditor():
    def __init__(self, player):
        self.player = player
        self.isPlaying = False
        self.level = Level()
        self.num_tiles = 33
        self.img_list = []
        self.img_list_rects = []
        for x in range(self.num_tiles+1):
            img = pygame.image.load(resource_path(f'assets/tiles/tile{x}.png'))
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            self.img_list.append(img)
        self.img_list.append(pygame.image.load(resource_path(f'assets/player/Player Blue/playerBlue_stand.png')))

        self.selected_idx = None
        self.top_of_selection = 0

        self.up_arrow = pygame.image.load(resource_path('assets/tiles/up_arrow.png'))
        self.up_arrow = pygame.transform.scale(self.up_arrow, (TILE_SIZE, TILE_SIZE))
        self.up_arrow_rect = self.up_arrow.get_rect()
        self.up_arrow_rect = self.up_arrow_rect.move((SCREEN_WIDTH - TILE_SIZE, 0))
        self.down_arrow = pygame.image.load(resource_path('assets/tiles/down_arrow.png'))
        self.down_arrow = pygame.transform.scale(self.down_arrow, (TILE_SIZE, TILE_SIZE))
        self.down_arrow_rect = self.down_arrow.get_rect()
        self.down_arrow_rect = self.down_arrow_rect.move((SCREEN_WIDTH - TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE - TILE_SIZE))

        self.back_button_img = pygame.image.load(resource_path('assets/tiles/back_button.png'))
        self.back_button_img = pygame.transform.scale(self.back_button_img, (TILE_SIZE, TILE_SIZE))
        self.back_button_rect = self.back_button_img.get_rect()
        self.back_button_rect = self.back_button_rect.move((0, 0))

        self.help_button_img = pygame.image.load(resource_path('assets/tiles/help_button.png'))
        self.help_button_img = pygame.transform.scale(self.help_button_img, (TILE_SIZE, TILE_SIZE))
        self.help_button_rect = self.help_button_img.get_rect()
        self.help_button_rect = self.help_button_rect.move((SCREEN_WIDTH - TILE_SIZE - TILE_SIZE - TILE_SIZE, 0))
        self.help_shown = False

        self.number_tiles_to_render = (SCREEN_HEIGHT - TILE_SIZE - TILE_SIZE) // TILE_SIZE
        for i in range(self.number_tiles_to_render):
            self.img_list_rects.append(pygame.Rect(SCREEN_WIDTH - TILE_SIZE, TILE_SIZE + i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        self.play_button_img = pygame.image.load(resource_path('assets/tiles/play_button.png'))
        self.play_button_img = pygame.transform.scale(self.play_button_img, (TILE_SIZE, TILE_SIZE))
        self.play_button_rect = self.play_button_img.get_rect()
        self.play_button_rect = self.play_button_rect.move((SCREEN_WIDTH - TILE_SIZE - TILE_SIZE, 0))

        self.stop_button_img = pygame.image.load(resource_path('assets/tiles/stop_button.png'))
        self.stop_button_img = pygame.transform.scale(self.stop_button_img, (TILE_SIZE, TILE_SIZE))
        self.stop_button_rect = self.stop_button_img.get_rect()
        self.stop_button_rect = self.stop_button_rect.move((SCREEN_WIDTH - TILE_SIZE - TILE_SIZE, 0))

    def render(self, screen):
        # render side bar
        for i in range(self.top_of_selection, self.top_of_selection + self.number_tiles_to_render-1):
            if i < self.num_tiles:
                screen.blit(self.img_list[i], (SCREEN_WIDTH - TILE_SIZE, TILE_SIZE + (i-self.top_of_selection) * TILE_SIZE))

        # render up arrow at the top
        screen.blit(self.up_arrow, self.up_arrow_rect)
        # render down arrow at the bottom
        screen.blit(self.down_arrow, self.down_arrow_rect)

        # render back button in top left
        screen.blit(self.back_button_img, self.back_button_rect)

        # render help button
        # screen.blit(self.help_button_img, self.help_button_rect)

        # Render start button in top right
        if not self.isPlaying:
            screen.blit(self.play_button_img, self.play_button_rect)
        else:
            screen.blit(self.stop_button_img, self.stop_button_rect)

        if self.help_shown:
            self.render_help(screen)

    def render_help(self, screen):
        pass

    def write_to_csv(self, x, y, tile_type):
        self.level.write_to_csv(x, y, tile_type)

    def set_player(self, x, y):
        self.level.set_player(x, y)
        self.player.x = x * TILE_SIZE
        self.player.y = y * TILE_SIZE
        self.player.starting_x = x
        self.player.starting_y = y

    def handle_events(self, offset) -> GameState:
        if self.isPlaying:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.right()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.holding_jump()
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player.down()
            if keys[pygame.K_SPACE]:
                pass

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.help_shown = False

            if self.isPlaying:
                self.player.isWalking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.left()
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.right()
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.jump(game_state=GameState.GAME)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player.down()
                    elif event.key == pygame.K_x:
                        self.player.dash()
                    elif event.key == pygame.K_z:
                        self.player.teleport()
                    elif event.key == pygame.K_r:
                        self.player.reset()

                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()

            if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
                pos = pygame.mouse.get_pos()
                if self.play_button_rect.collidepoint(pos):
                    self.isPlaying = not self.isPlaying
                elif self.down_arrow_rect.collidepoint(pos):
                    self.top_of_selection -= 1
                elif self.up_arrow_rect.collidepoint(pos):
                    self.top_of_selection += 1
                elif self.back_button_rect.collidepoint(pos):
                    return GameState.MAIN_MENU
                elif self.help_button_rect.collidepoint(pos):
                    self.help_shown = True
                else:
                    for rect in self.img_list_rects:
                        if rect.collidepoint(pos):
                            self.selected_idx = (self.img_list_rects.index(rect) + self.top_of_selection) % (self.num_tiles + 1)
                            break
                    else: # no tile was selected
                        nearest_tile = (int(pos[0]-offset) // TILE_SIZE, pos[1] // TILE_SIZE)
                        # place tile
                        if self.selected_idx != None and self.selected_idx != 33:
                            self.write_to_csv(nearest_tile[0], nearest_tile[1], self.selected_idx)
                        elif self.selected_idx == 33:
                            self.set_player(nearest_tile[0], nearest_tile[1])
            elif (event.type == pygame.MOUSEBUTTONUP and event.button == 3):
                pos = pygame.mouse.get_pos()
                nearest_tile = (int(pos[0]-offset) // TILE_SIZE, pos[1] // TILE_SIZE)
                self.write_to_csv(nearest_tile[0], nearest_tile[1], -1)
        return GameState.LEVEL_EDITOR
    
class LevelSelector():
    def __init__(self, screen):
        self.screen = screen
        self.load_levels()
        self.back_button_img = pygame.image.load(resource_path('assets/tiles/back_button.png'))
        self.back_button_img = pygame.transform.scale(self.back_button_img, (TILE_SIZE, TILE_SIZE))
        self.back_button_rect = self.back_button_img.get_rect()
        self.back_button_rect = self.back_button_rect.move((0, 0))

    def load_levels(self):
        self.level_names = [f for f in listdir(resource_path('assets/levels')) if f[len(f)-1] == 'v' and isfile(resource_path('assets/levels/' + f))]
        self.json_levels = [f for f in listdir(resource_path('assets/levels')) if f[len(f)-1] == 'n' and isfile(resource_path('assets/levels/' + f))]

    def render(self):
        level_rects = []
        delete_rects = []
        font = pygame.font.SysFont('Segoe UI Black', 30)

        # Render "Select Level" text at top of screen
        text = font.render("Select Level", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect = text_rect.move((SCREEN_WIDTH // 2 - text_rect.width // 2, 50))
        self.screen.blit(text, text_rect)


        for i, level in enumerate(self.level_names):
            # render text with white background
            text = font.render(level, True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect = text_rect.move((SCREEN_WIDTH // 2 - text_rect.width // 2, 100 + i * 50))
            pygame.draw.rect(self.screen, (255, 255, 255), text_rect)
            self.screen.blit(text, text_rect)
            level_rects.append(text_rect)

            # render delete button next to the right
            text = font.render("Delete", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect = text_rect.move((0, 100 + i * 50))
            pygame.draw.rect(self.screen, (255, 255, 255), text_rect)
            self.screen.blit(text, text_rect)
            delete_rects.append(text_rect)

        # render back button
        self.screen.blit(self.back_button_img, self.back_button_rect)

        return level_rects, delete_rects

    def load_player_pos(self, level_idx):
        with open(resource_path('assets/levels/' + self.json_levels[level_idx]), 'r') as f:
            data = json.load(f)
        return data['playerx'], data['playery']
    
    def delete_level(self, level_idx):
        os.remove(resource_path('assets/levels/' + self.level_names[level_idx]))
        os.remove(resource_path('assets/levels/' + self.json_levels[level_idx]))
        self.load_levels()