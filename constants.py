import enum

class GameState(enum.Enum):
	MAIN_MENU = 1
	PAUSE = 2
	GAME = 3
	SHOP = 4
	WIN = 5
	SETTINGS = 6


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

FPS = 60

#define game variables
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS

tutorial_descriptions = ["You're doing great! But\ncan you get a TEN SECOND TIME?", "Can't go this way, maybe\n a powerup might help?", "Powerups can unlock different\nroutes,or help you win faster", "Dying is part of the process,\nbut who's really keeping track?", "Get to the flag in 10 seconds to \nwin! And if you don't, choose a \npowerup to help you next time!", "Bugs please contact me:)"]

level_descriptions = ["Wow you came here to look at a sign?", "Hi~! Thanks for playing!", "Dedication really. Props to you~\n There's nothing here though", "You made it here! Have a cookie~", "Tip: You can press 'r' to restart", "Tip: you can combine dashing\n with teleporting to go farther", "Living dangerously?\nThat or you have a teleport", "And here we go again~"]
