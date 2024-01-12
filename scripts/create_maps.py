import json
import sys

from core.rest_query import create_interactomes_map, create_species_map, get_stats

stats_data = get_stats()

if stats_data is not None:
    print("Stats Dictionary:")
    print(stats_data)
else:
    print("Failed to fetch statistics.")
    sys.exit(1)

database_interactomes_count = stats_data.get('databaseInteractomesCount', 0)

interactomes_map = create_interactomes_map(database_interactomes_count, 'database')

if interactomes_map:
    with open('test/data/interactomes_map.json', 'w', encoding='utf-8') as file:
        json.dump(interactomes_map, file)
else:
    print("Failed to create interactomes map.")

predictomes_count = stats_data.get('predictomesCount', 0)

predictomes_map = create_interactomes_map(predictomes_count, 'predictome')

if predictomes_map:
    with open('test/data/predictomes_map.json', 'w', encoding='utf-8') as file:
        json.dump(predictomes_map, file)
else:
    print("Failed to create interactomes map.")

species_map = create_species_map()

if species_map:
    with open('test/data/species_map.json', 'w', encoding='utf-8') as file:
        json.dump(species_map, file)
else:
    print("Failed to create species map.")
