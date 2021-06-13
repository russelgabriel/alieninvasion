import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
	"""Overall class to manage game assets and behaviour"""

	def __init__(self):
		"""Initializes the game and creates game resources"""
		pygame.init()
		self.settings = Settings()
		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")
		self.ship = Ship(self)

	def run_game(self):
		"""Start main loop for the game"""

		while True:
			"""Start main loop for the game"""
			self._check_events()
			self.ship.update()
			self._update_screen()

	def _check_events(self):
		"""Respond to key presses and mouse clicks"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					# Move the ship to the right
					self.ship.moving_right = True
				if event.key == pygame.K_LEFT:
					# Move the ship to the left
					self.ship.moving_left = True
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT:
					# Stops the ship from moving to the right
					self.ship.moving_right = False
				if event.key == pygame.K_LEFT:
					# Stops the ship from moving to the left
					self.ship.moving_left = False

	def _update_screen(self):
		"""Updates images on the screen and flips to new screen"""
		# Redraw the screen after every loop
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()

		# Make the most recently drawn screen visible
		pygame.display.flip()


if __name__ == '__main__':
	# Make a game instance, and run the game
	ai = AlienInvasion()
	ai.run_game()
