import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.screens import SkillTreeScreen

class TestSkillTree(unittest.TestCase):
    def test_node_styles(self):
        screen = SkillTreeScreen()

        # Test start node style
        size, color = screen.get_node_style('start', False)
        self.assertEqual(size, (120, 120))
        self.assertEqual(color, (0.4, 0.3, 0.5, 1))

        size, color = screen.get_node_style('start', True)
        self.assertEqual(size, (120, 120))
        self.assertEqual(color, (0.7, 0.5, 0.9, 1))

        # Test notable node style
        size, color = screen.get_node_style('notable', False)
        self.assertEqual(size, (100, 100))
        self.assertEqual(color, (0.5, 0.4, 0.1, 1))

        size, color = screen.get_node_style('notable', True)
        self.assertEqual(size, (100, 100))
        self.assertEqual(color, (0.9, 0.7, 0.2, 1))

        # Test minor node style
        size, color = screen.get_node_style('minor', False)
        self.assertEqual(size, (60, 60))
        self.assertEqual(color, (0.5, 0.5, 0.5, 1))

        size, color = screen.get_node_style('minor', True)
        self.assertEqual(size, (60, 60))
        self.assertEqual(color, (0.2, 0.8, 0.2, 1))

        # Test keystone node style
        size, color = screen.get_node_style('keystone', False)
        self.assertEqual(size, (140, 140))
        self.assertEqual(color, (0.6, 0.1, 0.1, 1))

        size, color = screen.get_node_style('keystone', True)
        self.assertEqual(size, (140, 140))
        self.assertEqual(color, (1.0, 0.2, 0.2, 1))

if __name__ == '__main__':
    unittest.main()