from enum import Enum
from typing import List

class Format(Enum):
    SINGLE = 1
    MULTIPLE = 2

class SameSpeciesConfigLoader:
    SPECIES = 'Species'
    INTERACTOME_DATABASES = 'Interactome.Databases'
    INTERACTOME_MODIFIERS_22 = 'Interactome.Modifiers_22'
    INTERACTOME_POLYQ_22 = 'Interactome.polyQ_22'
    PREDICTOME_DATABASES = 'Predictome.Databases'
    PREDICTOME_MODIFIERS_22 = 'Predictome.Modifiers_22'
    PREDICTOME_POLYQ_22 = 'Predictome.polyQ_22'
    GENE_ID = 'GeneID'
    INT_LEVEL = 'Int_level'
    FORMAT = 'Format'

    def __init__(self, file_path):
        self.config = self.load_config(file_path)

    def load_config(self, file_path):
        config = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith('#') or len(line.strip()) == 0:
                    continue

                key, value = line.strip().split('=')
                key = key.strip()
                value = value.strip()

                if key.startswith('Interactome') or key.startswith('Predictome'):
                    value = [item.strip() for item in value.split(';')]
                    value = list(filter(lambda s: len(s) > 0, value))

                elif key == self.INT_LEVEL:
                    value = int(value)

                elif key == self.FORMAT:
                    if value == 'single':
                        value = Format.SINGLE
                    elif value == 'multiple':
                        value = Format.MULTIPLE
                    else:
                        raise ValueError('Invalid value for Format. Must be "single" or "multiple".')

                config[key] = value

        return config
    
    def get_species(self) -> str:
        if SameSpeciesConfigLoader.SPECIES in self.config:
            return self.config[SameSpeciesConfigLoader.SPECIES]
        
        raise ValueError(f'{SameSpeciesConfigLoader.SPECIES} not found')
    
    def get_gene_id(self) -> str:
        return self.config[SameSpeciesConfigLoader.GENE_ID]
    
    def get_interactions_level(self) -> str:
        return self.config[SameSpeciesConfigLoader.INT_LEVEL]
    
    def get_format(self) -> Format:
        return self.config[SameSpeciesConfigLoader.FORMAT]
    
    def get_interactomes(self) -> List[str]:
        toret = []

        toret.extend(self.config[SameSpeciesConfigLoader.INTERACTOME_DATABASES])
        toret.extend(self.config[SameSpeciesConfigLoader.INTERACTOME_MODIFIERS_22])
        toret.extend(self.config[SameSpeciesConfigLoader.INTERACTOME_POLYQ_22])

        return toret
    
    def get_predictomes(self) -> List[str]:
        toret = []

        toret.extend(self.config[SameSpeciesConfigLoader.PREDICTOME_DATABASES])
        toret.extend(self.config[SameSpeciesConfigLoader.PREDICTOME_MODIFIERS_22])
        toret.extend(self.config[SameSpeciesConfigLoader.PREDICTOME_POLYQ_22])

        return toret
    
    def __str__(self) -> str:
        return 'Configuration:\n' + '\n'.join([f'- {key}: {value}' for key, value in self.config.items()])
