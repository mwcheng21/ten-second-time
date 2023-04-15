
class PowerUp():
    def __init__(self, image):
        self.image = image
        self.description = "This is a powerup"

    def handle(self, player, timer):
        pass


class JumpPowerup(PowerUp):
    def __init__(self, image, jump_increase):
        self.image = image
        self.jump_increase = jump_increase
        self.description = f"Jump higher"

    def handle(self, player, timer):
        player.jump_starting_v -= self.jump_increase
        return player, timer

class IncreaseAcceleration(PowerUp):
    def __init__(self, image, accel_increase):
        self.image = image
        self.accel_increase = accel_increase
        self.description = f"Accelerate faster"

    def handle(self, player, timer):
        player.horizontal_gas_v += self.accel_increase
        return player, timer

class IncreaseMaxSpeed(PowerUp):
    def __init__(self, image, max_speed_increase):
        self.image = image
        self.max_speed_increase = max_speed_increase
        self.description = f"Max speed increased"

    def handle(self, player, timer):
        player.max_horizontal_v += self.max_speed_increase
        return player, timer

class TimeSlow(PowerUp):
    def __init__(self, image, slow_factor):
        self.image = image
        self.slow_factor = slow_factor
        self.description = f"Time moves {slow_factor} times slower"

    def handle(self, player, timer):
        timer.slow_down(self.slow_factor)
        return player, timer

class TimeStartsAt(PowerUp):
    def __init__(self, image, time):
        self.image = image
        self.time = time
        self.description = f"Subtract {time} from starting time"

    def handle(self, player, timer):
        timer.removed_time += self.time
        return player, timer

class TeleportPowerup(PowerUp):
    def __init__(self, image):
        self.image = image
        self.description = f"Teleport to short distances forward.\nPress 'z' to teleport"

    def handle(self, player, timer):
        player.canTeleport = True
        return player, timer
    

class DoubleJumpPowerup(PowerUp):
    def __init__(self, image):
        self.image = image
        self.description = f"Able to double jump"

    def handle(self, player, timer):
        player.canDoubleJump = True
        return player, timer
    

class DashPowerup(PowerUp):
    def __init__(self, image):
        self.image = image
        self.description = f"Dash forward.\nPress 'x' to dash"

    def handle(self, player, timer):
        player.canDash = True
        return player, timer
    
class ShrinkPowerup(PowerUp):
    def __init__(self, image):
        self.image = image
        self.description = f"Shrink"

    def handle(self, player, timer):
        player.shrink()
        return player, timer
    
