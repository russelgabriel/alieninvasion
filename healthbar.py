import pygame

class Healthbar:
	"""Health bar for when boss appears"""

	def __init__(self, ai_game, start_health):
		"""Initialize healthbar attributes"""

		super().__init__()

		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings

		self.width = 50
		self.red_color = (250, 0, 0)
		self.green_color = (0, 250, 0)

		self.green_rect = pygame.Rect(50, 75, 50, 750)

		self.start_health = start_health
		self.add = (1/self.start_health) * 750

	def dynamic_settings(self):
		self.red_length = 0

	def update_health_bar(self):
		self.red_length += self.add

	def draw_health_bar(self):
		"""Draw the bar on the screen"""

		# Create green rect
		self.red_rect = pygame.Rect(50, 75, 50, self.red_length)

		# Draw both rects
		pygame.draw.rect(self.screen, self.green_color, self.green_rect)
		pygame.draw.rect(self.screen, self.red_color, self.red_rect)
