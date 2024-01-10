import json

with open('maps/species_map.json', 'r') as file:
    species_map = json.load(file)

with open('maps/interactomes_map.json', 'r') as file:
    interactomes_map = json.load(file)

with open('maps/predictomes_map.json', 'r') as file:
    predictomes_map = json.load(file)

input_species = 'Homo sapiens'
input_interactome = 'BioGRID'
input_predictome = 'Based on Drosophila melanogaster BioGRID (DIOPT)'

print(input_species, species_map[input_species])
print(input_interactome, interactomes_map[species_map[input_species]][input_interactome])
print(input_predictome, predictomes_map[species_map[input_species]][input_predictome])