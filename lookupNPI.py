import pandas as pd
import requests

def fetch_taxonomies(npi):
    api_url = f"https://npiregistry.cms.hhs.gov/api/?version=2.1&number={npi}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            taxonomies = data['results'][0]['taxonomies']
            primary_taxonomy = [taxonomy['desc'] for taxonomy in taxonomies if taxonomy['primary'] == True]
            non_primary_taxonomies = [taxonomy['desc'] for taxonomy in taxonomies if taxonomy['primary'] == False]
            return primary_taxonomy, non_primary_taxonomies
    return None, None


def add_taxonomy_to_excel(npi_list_file):
    npi_data = pd.read_excel(npi_list_file)  # Read the Excel file

    npi_numbers = npi_data['NPI'].tolist()  # Extract the NPI numbers from the 'NPI' column

    primary_taxonomies = []
    non_primary_taxonomies = []
    # Loop through each NPI number and fetch the corresponding taxonomies
    for npi in npi_numbers:
        primary_taxonomy, non_primary_taxonomy = fetch_taxonomies(npi)
        primary_taxonomies.append(primary_taxonomy)
        non_primary_taxonomies.append(non_primary_taxonomy)

    # Add the 'Primary Taxonomies' column to the DataFrame
    npi_data['Primary Taxonomies'] = primary_taxonomies

    # Add the 'Non-Primary Taxonomies' column to the DataFrame
    npi_data['Non-Primary Taxonomies'] = non_primary_taxonomies

    # Save the updated DataFrame to the Excel file
    npi_data.to_excel(npi_list_file, index=False)


# Example usage
npi_list_file = 'npi_list.xlsx'  # Replace with the path to your Excel file

add_taxonomy_to_excel(npi_list_file)
