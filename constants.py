import enum

class GameState(enum.Enum):
	MAIN_MENU = 1
	PAUSE = 2
	GAME = 3
	SHOP = 4
	WIN = 5
	SETTINGS = 6
	TUTORIAL = 7


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

FPS = 60

#define game variables
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS