import requests

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

            for species in species_list:
                species_map[species['name']] = str(species['id'])
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.RequestException as e:
        print(f"Request failed: {e}")

    return species_map