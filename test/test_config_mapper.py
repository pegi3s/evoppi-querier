import json
import unittest

from core.config import SameSpeciesConfigLoader
from core.config_mapper import SameSpeciesConfigMapper

class TestSameSpeciesConfigMapper(unittest.TestCase):

    EXPECTED_QUERY_PARAMS =  [
        ('gene', '411'),
        ('maxDegree', '1'),
        ('interactome', '611'),
        ('interactome', '629'),
        ('interactome', '1193'),
        ('interactome', '1196'),
        ('interactome', '801'),
        ('interactome', '1032'),
        ('interactome', '1223')
    ]

    def test_map_config(self):
        file_path = 'test/config.txt'
        config_loader = SameSpeciesConfigLoader(file_path)

        with open('test/data/species_map.json', 'r', encoding='utf-8') as file:
            species_map = json.load(file)

        with open('test/data/interactomes_map.json', 'r', encoding='utf-8') as file:
            interactomes_map = json.load(file)

        with open('test/data/predictomes_map.json', 'r', encoding='utf-8') as file:
            predictomes_map = json.load(file)

        config_mapper = SameSpeciesConfigMapper(config_loader, species_map, interactomes_map, predictomes_map)

        self.assertListEqual(self.EXPECTED_QUERY_PARAMS, config_mapper.get_evoppi_query_params())
        

