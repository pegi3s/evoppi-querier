import json
import requests
import time

from core.config import SameSpeciesConfigLoader, Format
from core.config_mapper import SameSpeciesConfigMapper
from core.results_parser import json_results_to_csv

URL_API_BASE = 'http://evoppi.i3s.up.pt/evoppi-backend/rest/api'
URL_API_INTERACTIONS = f'{URL_API_BASE}/interaction'
URL_API_STATS = f'{URL_API_BASE}/database/stats'
URL_API_INTERACTOME = f'{URL_API_BASE}/interactome'
URL_API_SPECIES = f'{URL_API_BASE}/species'

def get_stats():
    response = requests.get(URL_API_STATS, timeout=120)

    if response.status_code == 200:
        return response.json()
    else:
        raise RuntimeError(f'Error: {response.status_code} - {response.text}')

def create_interactomes_map(database_interactomes_count, interactome_type='database'):
    base_url = f'{URL_API_INTERACTOME}/{interactome_type}'
    batch_size = 50
    interactomes_map = {}

    num_batches = (database_interactomes_count + batch_size - 1) // batch_size

    for batch_num in range(num_batches):
        start_index = batch_num * batch_size
        end_index = min((batch_num + 1) * batch_size, database_interactomes_count)

        params = {'start': start_index, 'end': end_index}

        try:
            response = requests.get(base_url, params=params, timeout=120)

            if response.status_code == 200:
                batch_interactomes = response.json()

                for interactome in batch_interactomes:
                    species_id = str(interactome['speciesA']['id'])
                    if not species_id in interactomes_map:
                        interactomes_map[species_id] = {}

                    interactomes_map[species_id][interactome['name']] = str(interactome['id'])
            else:
                raise RuntimeError(f'Error: {response.status_code} - {response.text}')

        except requests.RequestException as e:
            raise RuntimeError(f'Request failed: {e}')

    return interactomes_map

def create_species_map():
    species_map = {}

    try:
        response = requests.get(URL_API_SPECIES, timeout=120)

        if response.status_code == 200:
            species_list = response.json()

            for species in species_list:
                species_map[species['name']] = str(species['id'])
        else:
            raise RuntimeError(f'Error: {response.status_code} - {response.text}')

    except requests.RequestException as e:
        raise RuntimeError(f'Request failed: {e}')

    return species_map

def get_all_maps():
    stats_data = get_stats()
    
    database_interactomes_count = stats_data.get('databaseInteractomesCount', 0)
    interactomes_map = create_interactomes_map(database_interactomes_count, 'database')

    predictomes_count = stats_data.get('predictomesCount', 0)
    predictomes_map = create_interactomes_map(predictomes_count, 'predictome')

    species_map = create_species_map()

    return species_map, interactomes_map, predictomes_map

def send_get_request(url, params=None):
    try:
        response = requests.get(url, params=params, timeout=360)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f'Error during GET request to {url}: {e}')

def extract_result_reference(json_response):
    if 'resultReference' in json_response:
        return json_response['resultReference']
    else:
        raise RuntimeError('Invalid or missing "resultReference" in the response')

def process_completed(response_json, result_reference_url):
    total_interactions = response_json.get('totalInteractions', 0)

    responses = []
    for page in range(1, (total_interactions // 10) + 1):
        page_url = f'{result_reference_url}?page={page}&pageSize=10'
        page_response = send_get_request(page_url)
        responses.append(page_response)

    return responses

def check_status(result_reference_url):
    while True:
        try:
            response_json = send_get_request(result_reference_url + '?page=0&pageSize=10')
            if response_json and 'status' in response_json:
                status = response_json['status']
                print(f'Current status: {status}')

                if status == 'COMPLETED':
                    break
                elif status == 'FAILED':
                    response_error = json.dumps(response_json, indent=2)
                    raise RuntimeError(f'fProcess failed. JSON Response:\n{response_error}')
            else:
                raise RuntimeError('Invalid or missing "status" in the JSON response.')
        except Exception as e:
            raise RuntimeError(f'An error occurred while checking status: {e}')

        time.sleep(10)
    
    return status, response_json

def query_single_species(config_mapper: SameSpeciesConfigMapper):
    initial_params = config_mapper.get_evoppi_query_params()

    try:
        response_json = send_get_request(URL_API_INTERACTIONS, params=initial_params)
        if response_json:
            result_reference = extract_result_reference(response_json)
            final_status, latest_response_json = check_status(result_reference)
    except Exception as e:
        print(f'An error occurred: {e}')

    if final_status == 'COMPLETED':
        return process_completed(latest_response_json, result_reference)

    return None
