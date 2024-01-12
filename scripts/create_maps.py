import json
import requests
import sys

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

def create_interactomes_map(database_interactomes_count, type='database'):
    base_url = f"http://evoppi.i3s.up.pt/evoppi-backend/rest/api/interactome/{type}"
    batch_size = 50
    interactomes_map = {}

    # Calculate the number of batches required
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
                    if not interactome['speciesA']['id'] in interactomes_map:
                        interactomes_map[interactome['speciesA']['id']] = {}

                    interactomes_map[interactome['speciesA']['id']][interactome['name']] = str(interactome['id'])
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

            # Create species map from name to id
            for species in species_list:
                species_map[species['name']] = str(species['id'])
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.RequestException as e:
        print(f"Request failed: {e}")

    return species_map

if __name__ == "__main__":
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
