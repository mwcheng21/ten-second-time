import enum
from constants import TILE_SIZE
import pygame

class WorldMap:
    def __init__(self, filename):
        self.tiles = []
        self.obstacle_list = []
        self.death_list = []
        self.tiles = []
        self.win_list = []
        self.plant_list = []
        self.help_list = []
        self.help_list_tiles = []
        img_list = []
        self.num_tiles = 32
        for x in range(self.num_tiles+1):
            img = pygame.image.load(f'assets/tiles/tile{x}.png')
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            img_list.append(img)
        self.load_map(filename, img_list)

    def load_map(self, csv_file, img_list):
        with open(csv_file) as f:
            for y, line in enumerate(f):
                for x, tile in enumerate(line.split(",")):
                    tile = int(tile)
                    if (tile >= 0):
                        img = img_list[tile]
                        img_rect = img.get_rect()
                        img_rect.x = x * TILE_SIZE
                        img_rect.y = y * TILE_SIZE
                        tile_data = (img, img_rect)

                        if (tile == 0):
                            self.tiles.append(tile_data)
                            self.help_list_tiles.append(tile_data)
                            self.help_list.append(HelpSign(x, len(self.help_list_tiles)-1))
                            self.help_list.sort(key=lambda x: x.x)
                        elif (tile > 0 and tile <= 6):
                            #plant tile
                            self.plant_list.append(tile_data)
                            self.tiles.append(tile_data)
                            pass
                        elif (tile == 7):
                            # door tile
                            self.win_list.append(tile_data)
                            self.tiles.append(tile_data)
                        elif (tile == 8 or tile == 9):
                            #danger tiles
                            self.tiles.append(tile_data)
                            self.death_list.append(tile_data)
                        elif (tile > 9 and tile <= 32):
                            #obstacle tile
                            self.tiles.append(tile_data)
                            self.obstacle_list.append(tile_data)
      
class HelpSignManager():
    def __init__(self) -> None:
        self.descriptions = []

class HelpSign():
    def __init__(self, x, idx):
        self.x = x
        self.idx = idx