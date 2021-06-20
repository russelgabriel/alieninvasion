import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	"""A class to manage the ship"""

	def __init__(self, ai_game):
		"""Initializes the ship and its starting position"""

		super().__init__()
		
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		# Load the ship image and get its rect
		self.image = pygame.image.load('Images/ship.bmp')
		self.rect = self.image.get_rect()
		# Start each new ship at the bottom of the screen
		self.rect.midbottom = self.screen_rect.midbottom
		# Store decimal value for ship's horizontal position
		self.x = float(self.rect.x)
		# Movement flags
		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""Updates the ships movement according to the flag"""
		# Updates the x value rather than the rect
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed

		# Update rect from self.x
		self.rect.x = self.x


	def center_ship(self):
		"""Center ship on screen"""

		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)

	def blitme(self):
		"""Draw ship at its current location"""
		self.screen.blit(self.image, self.rect)

