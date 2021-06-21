class Settings:
	"""A class to store all settings for Alien Invasion"""

	def __init__(self):
		"""Initializes game's static settings"""

		# Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)

		# Ship settings
		self.ship_limit = 3

		# Bullet settings
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 0

		# Alien settings
		self.fleet_drop_speed = 10
		
		# How quickly the game speeds up
		self.speedup_scale = 1.1

		# How quickly aliens increase in value
		self.score_scale = 1.5

		self.difficulty_level = 'easy'

	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game"""

		self.ship_speed = 1.5
		self.bullet_speed = 3.0
		self.alien_speed = 1.0
		self.boss_speed = 1.0

		# 1 is right, -1 is left
		self.fleet_direction = 1

		if self.difficulty_level == 'easy':
			self.ship_limit = 5
			self.bullets_allowed = 10
			self.ship_speed = 0.75
			self.bullet_speed = 1.5
			self.alien_speed = 0.5
			self.boss_speed = 1.0
		elif self.difficulty_level == 'medium':
			self.ship_limit = 3
			self.bullets_allowed = 3
			self.ship_speed = 1.5
			self.bullet_speed = 3.0
			self.alien_speed = 1.0
			self.boss_speed = 1.5
		elif self.difficulty_level == 'difficult':
			self.ship_limit = 2
			self.bullets_allowed = 3
			self.ship_speed = 3.0
			self.bullet_speed = 6.0
			self.alien_speed = 2.0
			self.boss_speed = 2.0

		# Scoring
		self.alien_points = 50
		self.boss_points = 1000

	def increase_speed(self):
		"""Increase speed and alien value settings"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
		self.boss_points = iny(self.boss_points * self.score_scale)



