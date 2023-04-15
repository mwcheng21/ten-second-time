from musicplayer import MusicPlayer
from player import Player
from powerups.powerup_manager import PowerUpManager
import pygame
from render import Renderer
from timer import PygameTimer, Timer
from world_map import HelpSignManager, WorldMap
from constants import GameState, tutorial_descriptions

pygame.init()

screen = pygame.display.set_mode( (800,600) )

font = pygame.font.SysFont(None, 32)

clock = pygame.time.Clock()

level_timer = Timer()
total_timer = Timer()
renderer = Renderer(screen)
world_map = WorldMap("level_data.csv")
player = Player(world_map)

powerup_manager = PowerUpManager(screen, player, level_timer)
running = True
game_state = GameState.MAIN_MENU
freezeTick = 50

help_manager = HelpSignManager()
main_menu_music_player = MusicPlayer("assets/audio/silver_seven_step.wav")
level_music_player = MusicPlayer("assets/audio/bedtime.wav")
pause_music_player = MusicPlayer("assets/audio/dawn.wav")
win_music_player = MusicPlayer("assets/audio/Olympus.wav")
musicPlayers = [main_menu_music_player, level_music_player, pause_music_player]

def load_level(level):
	global world_map, player, powerup_manager
	world_map = WorldMap(level)
	player = Player(world_map)
	powerup_manager = PowerUpManager(screen, player, level_timer)

	if level == "tutorial_data.csv":
		help_manager.descriptions = tutorial_descriptions
		powerup_manager.add_tutorial_powerups()
	else:
		help_manager.descriptions = []
		powerup_manager.add_level_powerups()

def level_start():
	global game_state, player, level_timer, powerup_manager

	level_timer.reset()
	level_timer.start()
	total_timer.start()
	level_music_player.reset()
	level_music_player.play(-1)

def render_game():
	# render background
	renderer.render_background()

	# render world
	renderer.render_world(world_map, player, help_manager)

	# render player
	renderer.render_player(player)

	player.isHoldingJump = False

	#render timer
	renderer.render_timer(level_timer.get_running_time(), font)

	#render update
	renderer.render_update()

def game_loop():
	global game_state, player, level_timer, powerup_manager, freezeTick
	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT] or keys[pygame.K_a]:
		player.left()
	if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
		player.right()
	if keys[pygame.K_UP] or keys[pygame.K_w]:
		player.holding_jump()
	if keys[pygame.K_DOWN] or keys[pygame.K_s]:
		player.down()
	if keys[pygame.K_SPACE]:
		pass

	for event in pygame.event.get():
		player.isWalking = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				player.left()
			elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				player.right()
			elif event.key == pygame.K_UP or event.key == pygame.K_w:
				player.jump(game_state=game_state)
			elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
				player.down()
			elif event.key == pygame.K_x:
				player.dash()
			elif event.key == pygame.K_z:
				player.teleport()
			elif event.key == pygame.K_SPACE:
				player.won = True
			
	player.update()
	if (player.won):
		level_timer.stop()
		total_timer.stop()
		freezeTick = 50
		game_state = GameState.SHOP
		if level_timer.get_running_time() <= 10:
			game_state = GameState.WIN
			win_music_player.reset()
			win_music_player.play(-1, 2, 2)

	render_game()

def shop_loop():
	global game_state, player, level_timer, powerup_manager, freezeTick
	#event loop
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				powerup_manager.selected -= 1
				MusicPlayer.play_switch()
			elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				powerup_manager.selected += 1
				MusicPlayer.play_switch()
			elif event.key == pygame.K_SPACE:
				MusicPlayer.play_powerup()
				level_music_player.reset()
				level_music_player.play(-1)
				player, level_timer = powerup_manager.select().handle(player, level_timer)
				game_state = GameState.GAME
				level_start()
				player.reset()
				renderer.reset()

	# Render background
	render_game()

	# Render powerups
	powerup_manager.render_powerups()

	# Render time
	powerup_manager.render_timer(level_timer.get_running_time())
	if freezeTick < 0:
		level_timer.running_time = max(0, level_timer.get_running_time() - 1)
		player.jump(game_state=game_state)
		player.update()

	if freezeTick == 0:
		player.reset()

	freezeTick -= 1
	# render description
	powerup_manager.render_description()

	powerup_manager.render_continue()

def pause_loop():
	global game_state
	#event loop
	game_loop()


def main_menu_loop():
	global game_state

	if not main_menu_music_player.is_playing():
		main_menu_music_player.reset()
		main_menu_music_player.play(-1)

	start_button, tutorial_button, quit_button = renderer.render_main_menu()
	#event loop

	for event in pygame.event.get():
		if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
			game_state = GameState.GAME
			level_start()
		if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
			pos = pygame.mouse.get_pos()
			MusicPlayer.click()
			if start_button.collidepoint(pos):
				game_state = GameState.GAME
				load_level("level_data.csv")
				level_start()
			elif tutorial_button.collidepoint(pos):
				game_state = GameState.GAME
				load_level("tutorial_data.csv")
				level_start()
			elif quit_button.collidepoint(pos):
				pygame.quit()
				quit()

def pause_loop():
	global game_state
	#event loop
	pass

def settings_loop():
	global game_state
	#event loop
	# sound settings
	# keybind settings?
	# fullscreen settings?
	# resolution settings?
	# back button
	# credits?

	pass

def win_loop():
	# render stats
	global game_state, player, level_timer, total_timer, powerup_manager
	continue_button = renderer.render_stats(level_timer.get_running_time(), total_timer.get_running_time(), player)
	for event in pygame.event.get():
		if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
			pos = pygame.mouse.get_pos()
			if continue_button.collidepoint(pos):
				game_state = GameState.MAIN_MENU
				player.reset()
				level_timer.reset()
				total_timer.reset()
				powerup_manager = PowerUpManager(screen, player, level_timer)
				main_menu_music_player.reset()
				main_menu_music_player.play(-1)

while running:
	if (game_state == GameState.MAIN_MENU):
		main_menu_loop()
	elif (game_state == GameState.PAUSE):
		pause_loop()
	elif (game_state == GameState.SHOP):
		shop_loop()
	elif (game_state == GameState.GAME):
		game_loop()
	elif (game_state == GameState.WIN):
		win_loop()
	elif (game_state == GameState.SETTINGS):
		settings_loop()

	renderer.update()
	pygame.display.update()
	clock.tick(60)