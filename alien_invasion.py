import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
	"""Overall class to manage game assets and behaviour"""

	def __init__(self):
		"""Initializes the game and creates game resources"""
		pygame.init()
		self.settings = Settings()
		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self._create_fleet()

	def run_game(self):
		"""Start main loop for the game"""

		while True:
			"""Start main loop for the game"""

			self._check_events()
			self.ship.update()
			self._update_bullets()
			self._update_screen()

	def _check_events(self):
		"""Respond to key presses and mouse clicks"""

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			if event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_keydown_events(self, event):
		"""Respond to key presses"""

		if event.key == pygame.K_RIGHT:
			# Move the ship to the right
			self.ship.moving_right = True
		if event.key == pygame.K_LEFT:
			# Move the ship to the left
			self.ship.moving_left = True
		if event.key == pygame.K_SPACE:
			self._fire_bullet()
		if event.key == pygame.K_q:
			sys.exit()

	def _check_keyup_events(self, event):
		"""Respond to key releases"""

		if event.key == pygame.K_RIGHT:
			# Stops the ship from moving to the right
			self.ship.moving_right = False
		if event.key == pygame.K_LEFT:
			# Stops the ship from moving to the left
			self.ship.moving_left = False

	def _fire_bullet(self):
		"""Create new bullet and add it to the bullets group"""

		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Updates position of bullets and deletes old bullets"""

		# Update bullet position
		self.bullets.update()

		# Get rid of bullets after they've dissappeared
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

	def _create_fleet(self):
		"""Create fleet of aliens"""

		# Make an alien
		alien = Alien(self)
		self.aliens.add(alien)


	def _update_screen(self):
		"""Updates images on the screen and flips to new screen"""

		# Redraw the screen after every loop
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		# Make the most recently drawn screen visible
		pygame.display.flip()


if __name__ == '__main__':
	# Make a game instance, and run the game
	ai = AlienInvasion()
	ai.run_game()
