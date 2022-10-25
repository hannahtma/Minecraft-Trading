from cave import Cave
from material import Material
import unittest
from random_gen import RandomGen

class TestCave(unittest.TestCase):
    """ Testing additional AVL functionality. """

    def setUp(self):
        pass

    def test_init(self):
        # checking a valid cave being created
        try:
            cave = Cave("Haemar's Shame", Material('Diamond Axe', 0.8))
        except Exception:
            raise AssertionError("Unable to instantiate cave with correct inputs")


if __name__ == '__main__':
    # seeding the pseudo-random generator
    RandomGen.set_seed(16)

    # running all the tests
    unittest.main()
