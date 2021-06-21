import pygame
from pygame.sprite import Sprite

class Boss(Sprite):
	"""A class to represent a boss alien"""

	def __init__(self, ai_game):
		"""Initialize boss atrributes"""
		super().__init__()
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings

		# Load alien image, resize, and get rect
		self.image = pygame.image.load('Images/alien.bmp').convert_alpha()
		self.image = pygame.transform.scale(self.image, (120, 120))
		self.rect = self.image.get_rect()

		# Start alien on top middle of screen
		self.rect.centerx = self.screen_rect.centerx
		self.rect.y = 50

		# Store alien's horizontal position
		self.x = float(self.rect.x)

	def update(self):
		"""Move the aliens right or left"""
		self.x += self.settings.boss_speed
		self.rect.x = self.x
		if self.rect.left < 0 or self.rect.right > self.screen_rect.right:
			self.settings.boss_speed *= -1
