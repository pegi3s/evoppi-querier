import requests
import time
import json

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

    # Print the initial JSON response
    print("Initial JSON Response:")
    print(json.dumps(response_json, indent=2))

    # Iterate over pages to retrieve all entries
    for page in range(1, (total_interactions // 10) + 1):
        page_url = f"{result_reference_url}?page={page}&pageSize=10"
        page_response = send_get_request(page_url)
        if page_response:
            print(f"\nPage {page} JSON Response:")
            print(json.dumps(page_response, indent=2))
        else:
            print(f"\nFailed to retrieve data for page {page}")

    print("Process completed successfully.")

def check_status(result_reference_url):
    while True:
        try:
            response_json = send_get_request(result_reference_url + "?page=0&pageSize=10")
            if response_json and 'status' in response_json:
                status = response_json['status']
                print(f"Current status: {status}")

                if status == "COMPLETED":
                    process_completed(response_json, result_reference_url)
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

if __name__ == "__main__":
    initial_api_url = "http://evoppi.i3s.up.pt/evoppi-backend/rest/api/interaction"
    initial_params = {
        'gene': 411,
        'interactome': 629,
        'maxDegree': 1
    }

    try:
        response_json = send_get_request(initial_api_url, params=initial_params)
        if response_json:
            result_reference = extract_result_reference(response_json)
            if result_reference:
                print(f"Result Reference: {result_reference}")

                # Check status
                check_status(result_reference)
    except Exception as e:
        print(f"An error occurred: {e}")
