from constants import ROWS, TILE_SIZE, GameState
from musicplayer import MusicPlayer


STARTING_X = 9
STARTING_Y = 12

class Player:
    def __init__(self, world_map):
        self.completions = 0
        self.deaths = 0
        self.x = STARTING_X * TILE_SIZE
        self.y = STARTING_Y * TILE_SIZE
        self.width = 45*0.6#45*0.6
        self.height = 45*0.6#54*0.6

        #movement variables
        self.horizontal_v = 0
        self.horizontal_gas_v = 5
        self.max_horizontal_v = 30
        self.isMovingRight = True
        self.isWalking = False

        # dash variables
        self.dash_v = 0
        self.dash_starting_v = 40
        self.isDashing = False
        self.isHoldingJump = False

        # teleport variables
        self.teleport_v = 0
        self.teleport_startin_v = 425
        self.isTeleporting = False

        #jump variables
        self.isJumping = False
        self.jumpsUsed = 0
        self.gravity = 4
        self.vertical_v = 0
        self.jump_starting_v = -30

        self.world_map = world_map
        self.won = False

        self.canTeleport = False
        self.canDoubleJump = False
        self.canWallJump = False
        self.canDash = False

        self.isDev = False
        if self.isDev:
            self.canTeleport = True
            self.canDoubleJump = True
            self.canWallJump = True
            self.canDash = True

    def win(self):
        self.completions += 1
        self.won = True

    def reset(self):
        self.won = False
        self.x = STARTING_X * TILE_SIZE
        self.y = STARTING_Y * TILE_SIZE
        self.vertical_v = 0
        self.horizontal_v = 0

    def left(self):
        self.horizontal_v = max(-self.max_horizontal_v, self.horizontal_v - self.horizontal_gas_v)
        self.isMovingRight = False
        self.isWalking = True

    def right(self):
        self.horizontal_v = min(self.max_horizontal_v, self.horizontal_v + self.horizontal_gas_v)
        self.isMovingRight = True
        self.isWalking = True

    def jump(self, game_state):
        if not self.isJumping:
            if (game_state == GameState.GAME):
                MusicPlayer.play_jump()
            self.isJumping = True
            self.vertical_v = self.jump_starting_v
            self.jumpsUsed += 1
        elif self.isJumping and self.canDoubleJump and self.jumpsUsed == 1:
            if (game_state == GameState.GAME):
                MusicPlayer.play_jump()
            self.vertical_v = self.jump_starting_v
            self.jumpsUsed += 1

    def holding_jump(self):
        self.isHoldingJump = True

    def down(self):
        pass

    def dash(self):
        if not self.canDash:
            return
        if not self.isDashing:
            MusicPlayer.play_dash()
            self.dash_v = self.dash_starting_v * (1 if self.isMovingRight else -1)
            self.isDashing = True

    def teleport(self):
        if not self.canTeleport:
            return
        if not self.isTeleporting:
            self.teleport_v = self.teleport_startin_v * (1 if self.isMovingRight else -1)
            self.isTeleporting = True

    def shrink(self):
        self.width *= 0.5
        self.height *= 0.5

    def update(self):
        # apply gravity
        self.vertical_v += self.gravity

        # apply friction
        self.horizontal_v = self.horizontal_v * 0.7
        self.dash_v = self.dash_v * 0.5
        self.teleport_v = self.teleport_v * 0.2

        if abs(self.dash_v) < 0.1:
            self.isDashing = False

        if abs(self.teleport_v) < 0.1:
            self.isTeleporting = False


        collidedX = False
        for tile in self.world_map.obstacle_list:
            _, rect = tile
            # Check for collision in the y direction

            if rect.colliderect(self.x, self.y + self.vertical_v, self.width, self.height):
                # Check if below the ground i.e. jumping
                if self.vertical_v < 0:
                    self.vertical_v = 0
                    self.y = rect.bottom

                if self.vertical_v > 0:
                    self.isJumping = False
                    self.jumpsUsed = 0
                    self.vertical_v = 0

            # Check for collision in the x direction
            if rect.colliderect(self.x + self.horizontal_v, self.y, self.width, self.height):
                # Check if to the left or right of the obstacle
                if self.horizontal_v > 0:
                    self.x = rect.left - self.width - 1
                    collidedX = True
                elif self.horizontal_v < 0:
                    self.x = rect.right + 1
                    collidedX = True
        

        # apply velocity
        if not collidedX:
            self.x += self.horizontal_v + self.dash_v
        if self.isTeleporting:
            self.x += self.teleport_v
        elif self.isHoldingJump and self.isDashing:
            self.y += -self.dash_v
        else:
            self.y += self.vertical_v

        # check if player has completed the level
        for tile in self.world_map.win_list:
            _, rect = tile
            if rect.colliderect(self.x, self.y, self.width, self.height):
                self.win()

        # Check if player has died
        if not self.isDev:
            if self.y > ROWS * TILE_SIZE:
                self.deaths += 1
                self.reset()
            for tile in self.world_map.death_list:
                _, rect = tile
                if rect.colliderect(self.x, self.y, self.width, self.height):
                    self.deaths += 1
                    self.reset()
                    
