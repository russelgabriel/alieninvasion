import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""A class representing a single alien from a fleet"""

	def __init__(self, ai_game):
		"""Initialize alien and starting position"""

		super().__init__()
		self.screen = ai_game.screen

		# Load the alien image and set its rect attribute
		self.image = pygame.image.load('Images/alien.bmp')
		self.rect = self.image.get_rect()

		# Start each alien at the top left of the screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# Store alien's exact horizontal position
		self.x = float(self.rect.x)