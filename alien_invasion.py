import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from boss import Boss

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
		self.bosses = pygame.sprite.Group()

		self._create_fleet()   
 
 		# Make play button
		self.play_button = Button(self, "Play")

		# Make difficulty buttons
		self._make_difficulty_buttons()

		# Make scoreboard to store game statistics
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

	def _make_difficulty_buttons(self):
		"""Make buttons that allow player to select difficulty level"""

		self.easy_button = Button(self, "Easy")
		self.medium_button = Button(self, "Medium")
		self.difficult_button = Button(self, "Difficult")

		#Position buttons so they dont overlap
		self.easy_button.rect.top = (
			self.play_button.rect.top + 1.5*self.play_button.rect.height)
		self.easy_button._update_msg_position()

		self.medium_button.rect.top = (
			self.easy_button.rect.top + 1.5*self.easy_button.rect.height)
		self.medium_button._update_msg_position()

		self.difficult_button.rect.top = (
			self.medium_button.rect.top + 1.5*self.medium_button.rect.height)
		self.difficult_button._update_msg_position()

	def run_game(self):
		"""Start main loop for the game"""

		while True:
			"""Start main loop for the game"""

			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_boss()
				self._update_aliens()

			self._update_screen()

	def _check_events(self):
		"""Respond to key presses and mouse clicks"""

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.stats._write_new_high_score()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			if event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)
				self._check_difficulty_buttons(mouse_pos)

	def _check_play_button(self, mouse_pos):
		"""Start new game when player clicks play"""

		button_clicked = self.play_button.rect.collidepoint(mouse_pos)

		if button_clicked and not self.stats.game_active:
			self._start_game()
			self.sb.prep_images()

	def _check_difficulty_buttons(self, mouse_pos):
		"""Set the appropriate game difficulty"""

		easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
		medium_button_clicked = self.medium_button.rect.collidepoint(
			mouse_pos)
		diff_button_clicked = self.difficult_button.rect.collidepoint(
				mouse_pos)
		if easy_button_clicked:
			self.settings.difficulty_level = 'easy'
		elif medium_button_clicked:
			self.settings.difficulty_level = 'medium'
		elif diff_button_clicked:
			self.settings.difficulty_level = 'difficult'

	def _start_game(self):
		"""Starts game when play button is pressed or P is pressed"""

		# Hide mouse cursor
		pygame.mouse.set_visible(False)

		self.settings.initialize_dynamic_settings()

		# Reset game stats
		self.stats.reset_stats()
		self.stats.game_active = True

		# Reset score
		self.sb.prep_score()

		# Get rid of remaining aliens and bullets
		self.aliens.empty()
		self.bullets.empty()

		# Create new fleet and center ship
		self._create_fleet()
		self.ship.center_ship()

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
		if event.key == pygame.K_p:
			self._start_game()
		if event.key == pygame.K_q:
			self.stats._write_new_high_score()
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

		self._check_bullet_collisions()

	def _check_bullet_collisions(self):
		"""Respond to bullet collisions"""

		# Check if any bullets hit an alien and get rid of bullet and alien
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()
			self.sb.prep_level()
		if not self.aliens and not self.bosses:
			self._start_new_level()

	def _start_new_level(self):
		"""Start a new level when there are no more aliens"""

		# Increment level by one and show level
		self.stats.level += 1
		self.sb.prep_level()

		# Destroy existing bullets and create new fleet
		self.bullets.empty()

		# Create boss or fleet depending on level
		if self.stats.level % 5 == 0:
			self._create_boss()
		else:
			self._create_fleet()

		# Increase difficulty
		self.settings.increase_speed()

	def _create_fleet(self):
		"""Create fleet of aliens"""

		# Make an alien and find number of aliens in a row
		# Spacing between each alien is one alien width
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (alien_width * 2)
		number_aliens = available_space_x // (alien_width * 2)

		# Determine the number of rows that can fit on the screen
		ship_height = self.ship.rect.height
		avilable_space_y = (
			self.settings.screen_height - (3 * alien_height) - ship_height)
		number_rows = avilable_space_y // (alien_height * 2)

		# Create full fleet of aliens
		for row_number in range(number_rows):
			for alien_number in range(number_aliens):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		"""Create an alien and place it in a row"""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien_height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Respond appropriately if alien touches edge"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Drop the entire fleet and change fleet direction"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _check_aliens_bottom(self):
		"""Check if any aliens reach the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# Treat this the same as a ship collision with alien
				self._ship_hit()
				break

	def _update_aliens(self):
		"""Check if fleet is at an edge, then update position of all aliens"""
		self._check_fleet_edges()
		self.aliens.update()

		# Look for alien-ship collisions
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		# Look for aliens reaching bottom of the screen
		self._check_aliens_bottom()

	def _create_boss(self):
		boss = Boss(self)
		self.bosses.add(boss)

	def _update_boss(self):
		self.bosses.update()

	def _ship_hit(self):
		"""Respond to ship hit by alien"""

		if self.stats.ships_left > 1:
			# Decrement ships_left
			self.stats.ships_left -= 1
			self.sb.prep_ships()

			# Get rid of remaining bullets and aliens
			self.aliens.empty()
			self.bullets.empty()

			# Create new fleet and center ship
			self._create_fleet()
			self.ship.center_ship()
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

		# Pause
		sleep(0.5)

	def _update_screen(self):
		"""Updates images on the screen and flips to new screen"""

		# Redraw the screen after every loop
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)
		self.bosses.draw(self.screen)
		self.sb.show_score()

		if not self.stats.game_active:
			self.play_button.draw_button()
			self.easy_button.draw_button()
			self.medium_button.draw_button()
			self.difficult_button.draw_button()

		# Make the most recently drawn screen visible
		pygame.display.flip()


if __name__ == '__main__':
	# Make a game instance, and run the game
	ai = AlienInvasion()
	ai.run_game()
