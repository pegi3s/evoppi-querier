import json

from core.rest_query import get_all_maps

species_map, interactomes_map, predictomes_map = get_all_maps()

with open('test/data/interactomes_map.json', 'w', encoding='utf-8') as file:
    json.dump(interactomes_map, file)

with open('test/data/predictomes_map.json', 'w', encoding='utf-8') as file:
    json.dump(predictomes_map, file)

with open('test/data/species_map.json', 'w', encoding='utf-8') as file:
    json.dump(species_map, file)
