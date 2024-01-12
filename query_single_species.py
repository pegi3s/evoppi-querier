import click

from core.config import SameSpeciesConfigLoader, Format
from core.config_mapper import SameSpeciesConfigMapper
from core.rest_query import get_all_maps, query_single_species
from core.results_parser import json_results_to_csv

@click.command()
@click.option('--input', '-i', required=True, type=click.Path(exists=True), help='Input configuration file')
@click.option('--output', '-o', required=True, type=click.Path(), help='Output directory')
def process_data(input, output):
    """
    Process data based on the input configuration file and save the result in the output directory.
    """
    click.echo(f"Processing data from {input} and saving results to {output}")

    config_loader = SameSpeciesConfigLoader(input)

    species_map, interactomes_map, predictomes_map = get_all_maps()

    config_mapper = SameSpeciesConfigMapper(config_loader, species_map, interactomes_map, predictomes_map)

    results = query_single_species(config_mapper)

    if results:
        json_results_to_csv(results, config_loader.get_format(), output)

if __name__ == '__main__':
    process_data()
