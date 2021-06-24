import pygame

class Healthbar:
	"""Health bar for when boss appears"""

	def __init__(self, ai_game, start_health):
		"""Initialize healthbar attributes"""

		super().__init__()

		self.screen = ai_game.screen
		self.settings = ai_game.settings

		self.length = 800
		self.width = 50
		self.red_color = (250, 0, 0)
		self.green_color = (0, 250, 0)

		self.red_rect = pygame.Rect(75, 50, 50, 750)

		self.start_health = start_health

	# TODO create method to decrease health after every boss collision

	def draw_health_bar(self):
		"""Draw the bar on the screen"""

		# Create red rect
		pygame.draw.rect(self.screen, self.red_color, self.red_rect)

		pygame.draw.rect(self.screen, self.green_color, self.green_rect)
