import unittest

from core.config import Format
from core.config import SameSpeciesConfigLoader

class TestSameSpeciesConfigLoader(unittest.TestCase):

    def test_load_config(self):
        file_path = 'test/config.txt'
        config_loader = SameSpeciesConfigLoader(file_path)
        self.assertEqual(config_loader.get_species(), 'Homo sapiens')
        self.assertEqual(config_loader.get_format(), Format.SINGLE)
        self.assertEqual(len(config_loader.get_interactomes()), 4)
        self.assertEqual(len(config_loader.get_predictomes()), 3)
