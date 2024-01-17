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

    def run_missing(self, file_path, exception_message):
        with self.assertRaisesRegex(ValueError, exception_message):
            SameSpeciesConfigLoader(file_path)

    def test_map_config_missing_species(self):
        self.run_missing('test/config_missing_species.txt', r'Species not found')
    
    def test_map_config_missing_geneid(self):
        self.run_missing('test/config_missing_geneid.txt', r'GeneID not found')

    def test_map_config_missing_int_level(self):
        self.run_missing('test/config_missing_int_level.txt', r'Int_level not found')

    def test_map_config_missing_format(self):
        self.run_missing('test/config_missing_format.txt', r'Format not found')
