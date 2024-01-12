import requests
import time
import json

from core.config import SameSpeciesConfigLoader, Format
from core.config_mapper import SameSpeciesConfigMapper
from core.results_parser import json_results_to_csv

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
    # json_results_to_csv(responses, Format.SINGLE, 'query.csv')
    json_results_to_csv(responses, Format.MULTIPLE, '/tmp/results')

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

if __name__ == "__main__":
    initial_api_url = "http://evoppi.i3s.up.pt/evoppi-backend/rest/api/interaction"
    """
    initial_params = {
        'gene': 411,
        'interactome': 629,
        'maxDegree': 1
    }
    initial_params = [
        ('gene', 411),
        ('interactome', 629),
        ('interactome', 615),
        ('maxDegree', 1)
    ]
    """

    file_path = 'test/config.txt'
    config_loader = SameSpeciesConfigLoader(file_path)

    with open('test/data/species_map.json', 'r', encoding='utf-8') as file:
        species_map = json.load(file)

    with open('test/data/interactomes_map.json', 'r', encoding='utf-8') as file:
        interactomes_map = json.load(file)

    with open('test/data/predictomes_map.json', 'r', encoding='utf-8') as file:
        predictomes_map = json.load(file)

    config_mapper = SameSpeciesConfigMapper(config_loader, species_map, interactomes_map, predictomes_map)

    initial_params=config_mapper.get_evoppi_query_params()

    try:
        response_json = send_get_request(initial_api_url, params=initial_params)
        if response_json:
            result_reference = extract_result_reference(response_json)
            if result_reference:
                print(f"Result Reference: {result_reference}")

                # Check status
                final_status, latest_response_json = check_status(result_reference)
    except Exception as e:
        print(f"An error occurred: {e}")

    if final_status == 'COMPLETED':
        process_completed(latest_response_json, result_reference)
