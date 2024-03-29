from core.config import SameSpeciesConfigLoader
from typing import Dict, List

class SameSpeciesConfigMapper:
    
    def __init__(
            self, 
            config: SameSpeciesConfigLoader, 
            species_mapping: Dict, 
            interactomes_mapping: Dict,
            predictomes_mapping: Dict
        ):
        self.config = config
        self.species_mapping = species_mapping
        self.interactomes_mapping = interactomes_mapping
        self.predictomes_mapping = predictomes_mapping
        self.species_id = self.find_species_id()
        self.query_params = self._get_evoppi_query_params()

    def get_config(self) -> SameSpeciesConfigLoader:
        return self.config

    def find_species_id(self) -> str:
        species = self.config.get_species()
        if species in self.species_mapping:
            return self.species_mapping[species]
        else:
            raise ValueError(f'Invalid value for species ({species}). It is unknown.')

    def get_interactome_id_params(self, mapping: Dict, interactomes: List[str]):
        toret = []

        if self.species_id in mapping:
            species_interactomes = mapping[self.species_id]
        else:
            raise ValueError(f'No interactomes found for the specified species ({self.config.get_species()}).')

        for interactome in interactomes:
            if interactome in species_interactomes:
                toret.append((
                    'interactome',
                    species_interactomes[interactome]['id']
                ))
            else:
                raise ValueError(f'Invalid interactome name ({interactome}). No interactome found for the specified species ({self.config.get_species()}).')

        return toret

    def _get_evoppi_query_params(self):
        query_params = [
            ('gene', self.config.get_gene_id()),
            ('maxDegree', str(self.config.get_interactions_level()))
        ]

        interactomes = []
        interactomes.extend(
            self.get_interactome_id_params(self.interactomes_mapping, self.config.get_interactomes()),
        )
        interactomes.extend(
            self.get_interactome_id_params(self.predictomes_mapping, self.config.get_predictomes())
        )

        if len(interactomes) == 0:
            raise ValueError('There should be at least one interactome or predictome')
        else:
            query_params.extend(interactomes)
        
        return query_params
    
    def get_evoppi_query_params(self):
        return self.query_params
