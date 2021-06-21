class GameStats:
	"""Track statistics for alien invasion"""

	def __init__(self, ai_game):
		"""Initialize statistics"""

		self.settings = ai_game.settings
		self.reset_stats()

		# Start alien invasion in an inactive state
		self.game_active = False

		# Get high score from txt file
		self._get_high_score()

	def reset_stats(self):
		"""Initialize statistics that can change during game"""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 4

	def _get_high_score(self):
		with open('high_score.txt') as f:
			score = f.read()
			self.high_score = int(score)

	def _write_new_high_score(self):
		with open('high_score.txt', 'w') as f:
			f.write(str(self.high_score))