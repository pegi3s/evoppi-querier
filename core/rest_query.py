import requests
import time

from core.config import SameSpeciesConfigLoader, Format
from core.config_mapper import SameSpeciesConfigMapper
from core.results_parser import json_results_to_csv

def get_stats():
    url = "http://evoppi.i3s.up.pt/evoppi-backend/rest/api/database/stats"

    try:
        response = requests.get(url, timeout=120)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def create_interactomes_map(database_interactomes_count, interactome_type='database'):
    base_url = f"http://evoppi.i3s.up.pt/evoppi-backend/rest/api/interactome/{interactome_type}"
    batch_size = 50
    interactomes_map = {}

    num_batches = (database_interactomes_count + batch_size - 1) // batch_size

    for batch_num in range(num_batches):
        start_index = batch_num * batch_size
        end_index = min((batch_num + 1) * batch_size, database_interactomes_count)

        params = {"start": start_index, "end": end_index}

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
                print(f"Error: {response.status_code} - {response.text}")

        except requests.RequestException as e:
            print(f"Request failed: {e}")

    return interactomes_map

def create_species_map():
    url = "http://evoppi.i3s.up.pt/evoppi-backend/rest/api/species"
    species_map = {}

    try:
        response = requests.get(url, timeout=120)

        if response.status_code == 200:
            species_list = response.json()

            for species in species_list:
                species_map[species['name']] = str(species['id'])
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.RequestException as e:
        print(f"Request failed: {e}")

    return species_map

def get_all_maps():
    stats_data = get_stats()
    if stats_data is None:
        raise RuntimeError('Error fetching EvoPPI statistics. Please, check network status')
    
    database_interactomes_count = stats_data.get('databaseInteractomesCount', 0)

    interactomes_map = create_interactomes_map(database_interactomes_count, 'database')

    if not interactomes_map:
        raise RuntimeError('Error fetching EvoPPI interactomes. Please, check network status')

    predictomes_count = stats_data.get('predictomesCount', 0)

    predictomes_map = create_interactomes_map(predictomes_count, 'predictome')

    if not predictomes_map:
        raise RuntimeError('Error fetching EvoPPI predictomes. Please, check network status')

    species_map = create_species_map()

    if not species_map:
        raise RuntimeError('Error fetching EvoPPI species. Please, check network status')

    return species_map, interactomes_map, predictomes_map


def send_get_request(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during GET request: {e}")
        return None

def extract_result_reference(json_response):
    if 'resultReference' in json_response:
        return json_response['resultReference']
    else:
        print("No 'resultReference' key found in the JSON response.")
        return None

def process_completed(response_json, result_reference_url):
    total_interactions = response_json.get('totalInteractions', 0)
    print(f"Total Interactions: {total_interactions}")

    # Iterate over pages to retrieve all entries
    responses = []
    for page in range(1, (total_interactions // 10) + 1):
        page_url = f"{result_reference_url}?page={page}&pageSize=10"
        page_response = send_get_request(page_url)
        if page_response:
            # print(f"\nPage {page} JSON Response:")
            # print(json.dumps(page_response, indent=2))
            responses.append(page_response)
        else:
            print(f"\nFailed to retrieve data for page {page}")

    print("Process completed successfully.")
    print(f'Got {len(responses)} page responses')
    return responses

def check_status(result_reference_url):
    while True:
        try:
            response_json = send_get_request(result_reference_url + "?page=0&pageSize=10")
            if response_json and 'status' in response_json:
                status = response_json['status']
                print(f"Current status: {status}")

                if status == "COMPLETED":
                    break
                elif status == "FAILED":
                    print("Process failed. JSON Response:")
                    print(json.dumps(response_json, indent=2))
                    break
                else:
                    print("Invalid status in the JSON response.")
            else:
                print("Invalid or missing 'status' in the JSON response.")
        except Exception as e:
            print(f"An error occurred while checking status: {e}")

        time.sleep(5)  # Wait for 5 seconds before checking again
    
    return status, response_json

initial_api_url = "http://evoppi.i3s.up.pt/evoppi-backend/rest/api/interaction"

def query_single_species(config_mapper: SameSpeciesConfigMapper):
    initial_params = config_mapper.get_evoppi_query_params()

    try:
        response_json = send_get_request(initial_api_url, params=initial_params)
        if response_json:
            result_reference = extract_result_reference(response_json)
            if result_reference:
                print(f"Result Reference: {result_reference}")
                final_status, latest_response_json = check_status(result_reference)
    except Exception as e:
        print(f"An error occurred: {e}")

    if final_status == 'COMPLETED':
        return process_completed(latest_response_json, result_reference)
