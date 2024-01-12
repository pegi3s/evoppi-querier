import unittest
import tempfile

from core.results_parser import json_results_to_csv_multiple
from core.results_parser import json_results_to_csv_simple
from core.results_parser import write_interactions_to_csv

class TestResultsParser(unittest.TestCase):

    EVOPPI_SAME_SPECIES_JSON_RESULTS_RESPONSE = response = {
        "id": "e710dfc4-f623-42a7-9957-8373643b00ea",
        "queryGene": {
            "id": 411,
            "name": "ARSB",
            "uri": "http://evoppi.i3s.up.pt/evoppi-backend/rest/api/gene/411"
        },
        "queryMaxDegree": 1,
        "totalInteractions": 23,
        "status": "COMPLETED",
        "species": {
            "id": 16,
            "name": "Homo sapiens",
            "uri": "http://evoppi.i3s.up.pt/evoppi-backend/rest/api/species/16"
        },
        "interactomes": [
            {
            "id": 801,
            "name": "Based on Drosophila melanogaster BioGRID (DIOPT)",
            "uri": "http://evoppi.i3s.up.pt/evoppi-backend/rest/api/interactome/801"
            },
            {
            "id": 611,
            "name": "BioGRID",
            "uri": "http://evoppi.i3s.up.pt/evoppi-backend/rest/api/interactome/611"
            },
            {
            "id": 629,
            "name": "HIPPIE",
            "uri": "http://evoppi.i3s.up.pt/evoppi-backend/rest/api/interactome/629"
            },
            {
            "id": 1223,
            "name": "Homo sapiens Danio rerio (from DIOPT) (PolyQ_models_22)",
            "uri": "http://evoppi.i3s.up.pt/evoppi-backend/rest/api/interactome/1223"
            },
            {
            "id": 1032,
            "name": "Based on Drosophila melanogaster BioGRID (ENSEMBL)",
            "uri": "http://evoppi.i3s.up.pt/evoppi-backend/rest/api/interactome/1032"
            },
            {
            "id": 1193,
            "name": "Homo sapiens (Modifiers_22)",
            "uri": "http://evoppi.i3s.up.pt/evoppi-backend/rest/api/interactome/1193"
            },
            {
            "id": 1196,
            "name": "Homo sapiens (PolyQ_22)",
            "uri": "http://evoppi.i3s.up.pt/evoppi-backend/rest/api/interactome/1196"
            }
        ],
        "interactions": {
            "result": {
            "id": "e710dfc4-f623-42a7-9957-8373643b00ea",
            "uri": "http://evoppi.i3s.up.pt/evoppi-backend/rest/api/interaction/result/e710dfc4-f623-42a7-9957-8373643b00ea"
            },
            "filteringOptions": {
            "page": 2,
            "pageSize": 10,
            "orderField": "NONE",
            "sortDirection": "NONE",
            "interactomeId": None
            },
            "interactions": [
                {
                    "interactomeDegrees": [
                    {
                        "id": 1032,
                        "degree": 1
                    },
                    {
                        "id": 801,
                        "degree": 1
                    }
                    ],
                    "geneA": 411,
                    "geneAName": "ARSB",
                    "geneB": 79613,
                    "geneBName": "CCDS45516.1"
                },
                {
                    "interactomeDegrees": [
                    {
                        "id": 801,
                        "degree": 1
                    }
                    ],
                    "geneA": 411,
                    "geneAName": "ARSB",
                    "geneB": 645121,
                    "geneBName": "CCDS34236.1"
                },
                {
                    "interactomeDegrees": [
                    {
                        "id": 629,
                        "degree": 1
                    }
                    ],
                    "geneA": 411,
                    "geneAName": "ARSB",
                    "geneB": 728358,
                    "geneBName": "CCDS43691.1"
                }
            ]
        }
    }

    def test_json_results_to_csv_simple(self):
        expected_columns = ['geneA', 'geneAName', 'geneB', 'geneBName',
                            'Based on Drosophila melanogaster BioGRID (ENSEMBL)', # 1032
                            'Based on Drosophila melanogaster BioGRID (DIOPT)', # 801
                            'HIPPIE' # 629
                            ]
        expected_rows = [
            {'geneA': 411, 'geneAName': 'ARSB', 'geneB': 79613, 'geneBName': 'CCDS45516.1', 'Based on Drosophila melanogaster BioGRID (ENSEMBL)': 1, 'Based on Drosophila melanogaster BioGRID (DIOPT)': 1},
            {'geneA': 411, 'geneAName': 'ARSB', 'geneB': 645121, 'geneBName': 'CCDS34236.1', 'Based on Drosophila melanogaster BioGRID (DIOPT)': 1},
            {'geneA': 411, 'geneAName': 'ARSB', 'geneB': 728358, 'geneBName': 'CCDS43691.1', 'HIPPIE': 1}
        ]

        interactions = self.EVOPPI_SAME_SPECIES_JSON_RESULTS_RESPONSE['interactions']['interactions']
        interactomes = self.EVOPPI_SAME_SPECIES_JSON_RESULTS_RESPONSE['interactomes']
        columns_simple, rows_simple = json_results_to_csv_simple(interactions, interactomes)
        
        self.assertListEqual(expected_columns, columns_simple)
        self.assertListEqual(expected_rows, rows_simple)

    def test_json_results_to_csv_simple_write_file(self):
        interactions = self.EVOPPI_SAME_SPECIES_JSON_RESULTS_RESPONSE['interactions']['interactions']
        interactomes = self.EVOPPI_SAME_SPECIES_JSON_RESULTS_RESPONSE['interactomes']
        columns, rows = json_results_to_csv_simple(interactions, interactomes)

        with tempfile.NamedTemporaryFile(delete=False, mode='w+') as tmp_file:
            write_interactions_to_csv(columns, rows, tmp_file.name)

            with open(tmp_file.name, 'r', encoding='utf-8') as file:
                file_lines = file.readlines()
                self.assertEqual(len(file_lines), 4, "Number of lines in the file is not 4")


    def test_json_results_to_csv_multiple(self):
        expected_columns = [
            ['geneA', 'geneAName', 'geneB', 'geneBName', 'Based on Drosophila melanogaster BioGRID (ENSEMBL)'], # 1032
            ['geneA', 'geneAName', 'geneB', 'geneBName', 'Based on Drosophila melanogaster BioGRID (DIOPT)'], # 801
            ['geneA', 'geneAName', 'geneB', 'geneBName', 'HIPPIE'] # 629
        ]
        expected_rows = [
            [{'geneA': 411, 'geneAName': 'ARSB', 'geneB': 79613, 'geneBName': 'CCDS45516.1', 'Based on Drosophila melanogaster BioGRID (ENSEMBL)': 1}, {'geneA': 411, 'geneAName': 'ARSB', 'geneB': 645121, 'geneBName': 'CCDS34236.1', 'Based on Drosophila melanogaster BioGRID (ENSEMBL)': None}, {'geneA': 411, 'geneAName': 'ARSB', 'geneB': 728358, 'geneBName': 'CCDS43691.1', 'Based on Drosophila melanogaster BioGRID (ENSEMBL)': None}],
            [{'geneA': 411, 'geneAName': 'ARSB', 'geneB': 79613, 'geneBName': 'CCDS45516.1', 'Based on Drosophila melanogaster BioGRID (DIOPT)': 1}, {'geneA': 411, 'geneAName': 'ARSB', 'geneB': 645121, 'geneBName': 'CCDS34236.1', 'Based on Drosophila melanogaster BioGRID (DIOPT)': 1}, {'geneA': 411, 'geneAName': 'ARSB', 'geneB': 728358, 'geneBName': 'CCDS43691.1', 'Based on Drosophila melanogaster BioGRID (DIOPT)': None}],
            [{'geneA': 411, 'geneAName': 'ARSB', 'geneB': 79613, 'geneBName': 'CCDS45516.1', 'HIPPIE': None}, {'geneA': 411, 'geneAName': 'ARSB', 'geneB': 645121, 'geneBName': 'CCDS34236.1', 'HIPPIE': None}, {'geneA': 411, 'geneAName': 'ARSB', 'geneB': 728358, 'geneBName': 'CCDS43691.1', 'HIPPIE': 1}]
        ]

        interactions = self.EVOPPI_SAME_SPECIES_JSON_RESULTS_RESPONSE['interactions']['interactions']
        interactomes = self.EVOPPI_SAME_SPECIES_JSON_RESULTS_RESPONSE['interactomes']
        datasets_multiple = json_results_to_csv_multiple(interactions, interactomes)
        self.assertEqual(3, len(datasets_multiple))

        for index, dataset in enumerate(datasets_multiple, start=0):
            self.assertListEqual(expected_columns[index], dataset[0])
            self.assertListEqual(expected_rows[index], dataset[1])