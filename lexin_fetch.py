import requests
import json

def fetch_word_data(word):
    """
    Fetches data for a given word from the Lexin website.

    Args:
        word (str): The word to search for.

    Returns:
        requests.Response: The HTTP response object.
    """
    base_url = ("https://lexin.nada.kth.se/lexin/service"
        f"?searchinfo=both,swe_swe,{requests.utils.quote(word)}"
        "&output=JSON")
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Error: Failed to fetch data, status code {response.status_code}")

def remove_keys(data, keys_to_remove):
    if isinstance(data, dict):
        return {k: remove_keys(v, keys_to_remove) for k, v in data.items() if k not in keys_to_remove}
    elif isinstance(data, list):
        return [remove_keys(item, keys_to_remove) for item in data]
    else:
        return data

def extract_data_from_json(response_json):
    response_lean = remove_keys(response_json, keys_to_remove={"ID", "VariantID"})
    return response_lean

if __name__ == "__main__":
    response_json = fetch_word_data("gå")
    extracted_data = extract_data_from_json(response_json=response_json)
    print(extracted_data)