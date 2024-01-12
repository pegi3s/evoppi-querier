import csv
import os

from typing import List, Set, Dict

from core.config import Format

def extract_unique_ids(json_interactions: List) -> Set:
    unique_ids = set()
    for interaction in json_interactions:
        for interactome_degree in interaction["interactomeDegrees"]:
            unique_ids.add(interactome_degree["id"])

    return unique_ids

def get_interactomes_mapping(interactomes: List) -> Dict:
    return {i['id']:i['name'] for i in interactomes}

def json_results_to_csv_simple(json_interactions: List, interactomes: List):
    unique_ids = extract_unique_ids(json_interactions)
    interactomes_mapping = get_interactomes_mapping(interactomes)

    columns = ["geneA", "geneAName", "geneB", "geneBName"] + [interactomes_mapping[id] for id in unique_ids]
    rows = []

    for interaction in json_interactions:
        row_data = {
            "geneA": interaction["geneA"],
            "geneAName": interaction["geneAName"],
            "geneB": interaction["geneB"],
            "geneBName": interaction["geneBName"],
        }

        for interactome_degree in interaction["interactomeDegrees"]:
            interactome_name = interactomes_mapping[interactome_degree["id"]]
            row_data[interactome_name] = interactome_degree["degree"]

        rows.append(row_data)

    return columns, rows

def json_results_to_csv_multiple(json_interactions: List, interactomes: List):
    unique_ids = extract_unique_ids(json_interactions)
    interactomes_mapping = get_interactomes_mapping(interactomes)

    datasets = []

    for unique_id in unique_ids:
        columns = ["geneA", "geneAName", "geneB", "geneBName", interactomes_mapping[unique_id]]
        rows = []

        for interaction in json_interactions:
            row_data = {
                "geneA": interaction["geneA"],
                "geneAName": interaction["geneAName"],
                "geneB": interaction["geneB"],
                "geneBName": interaction["geneBName"],
            }

            degree = next(
                (item["degree"] for item in interaction["interactomeDegrees"] if item["id"] == unique_id),
                None,
            )

            if not degree is None:
                row_data[interactomes_mapping[unique_id]] = degree
                rows.append(row_data)

        datasets.append((columns, rows))

    return datasets

def write_interactions_to_csv(csv_columns: List, rows: List, csv_file_path: str):
    with open(csv_file_path, "w", newline="", encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()

        for row_data in rows:
            writer.writerow(row_data)

def json_results_to_csv(evoppi_responses: List, output_format: Format, output_path: str):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    interactions = []
    interactomes = evoppi_responses[0]['interactomes']

    for same_species_response in evoppi_responses:
        interactions.extend(same_species_response['interactions']['interactions'])

    if output_format is Format.SINGLE:
        columns, rows = json_results_to_csv_simple(interactions, interactomes)
        write_interactions_to_csv(columns, rows, f'{output_path}/EvoPPI_Results.csv')
    elif output_format is Format.MULTIPLE:
        datasets_multiple = json_results_to_csv_multiple(interactions, interactomes)

        for columns, rows in datasets_multiple:
            interactome_file_name = str(columns[len(columns)-1]).replace(' ', '_')
            write_interactions_to_csv(columns, rows, f'{output_path}/{interactome_file_name}.csv')
    