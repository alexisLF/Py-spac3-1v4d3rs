import unittest
import space

class TestClass(unittest.TestCase):
	
	def test_end_game(self):
		app = space.App()
		self.assertEqual(app.end, 0)

	def test_game_over(self):
		app = space.App()
		self.assertEqual(app.gameOver, -1)

	def test_player_name(self):
		player = space.App().player
		self.assertEqual(player.name, 'PLAYER1')

	def test_not_player_name(self):
		player = space.App().player
		self.assertNotEqual(player.name, 'PLAYER2')
		