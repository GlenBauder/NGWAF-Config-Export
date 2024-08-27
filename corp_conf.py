#!/usr/bin/python3
import requests
import json
import os

def get_corp_configuration(corp_name, cookies_dict):
    url = f"https://dashboard.signalsciences.net/api/v0/corps/{corp_name}/bulk"
    response = requests.get(url, cookies=cookies_dict)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve corp configuration for {corp_name}. Status code: {response.status_code}")
        return None

def get_sites(corp_name, cookies_dict):
    url = f"https://dashboard.signalsciences.net/api/v0/corps/{corp_name}/sites"
    response = requests.get(url, cookies=cookies_dict)
    if response.status_code == 200:
        return response.json().get("data", [])  # Access the "data" key and return an empty list if it doesn't exist
    else:
        print(f"Failed to retrieve sites for corp {corp_name}. Status code: {response.status_code}")
        return None

def get_site_configuration(corp_name, site_name, cookies_dict):
    url = f"https://dashboard.signalsciences.net/api/v0/corps/{corp_name}/sites/{site_name}/bulk"
    response = requests.get(url, cookies=cookies_dict)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve site configuration for {site_name} in corp {corp_name}. Status code: {response.status_code}")
        return None

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main(corp_name, cookies_dict):
    # Create a directory to store the output files
    output_dir = f"{corp_name}_config"
    os.makedirs(output_dir, exist_ok=True)

    # Get corp configuration
    corp_config = get_corp_configuration(corp_name, cookies_dict)
    if corp_config:
        corp_config_filename = os.path.join(output_dir, f"corp_{corp_name}_config.json")
        save_to_json(corp_config, corp_config_filename)
        print(f"Corp configuration saved to {corp_config_filename}")

    # Get sites
    sites = get_sites(corp_name, cookies_dict)
    if sites:
        for site in sites:
            site_name = site.get('name')
            if site_name:
                site_config = get_site_configuration(corp_name, site_name, cookies_dict)
                if site_config:
                    site_config_filename = os.path.join(output_dir, f"{site_name}_config.json")
                    save_to_json(site_config, site_config_filename)
                    print(f"Site configuration for {site_name} saved to {site_config_filename}")
                else:
                    print(f"Skipping site configuration for {site_name}")
            else:
                print("Site name not found in site data. Skipping.")

if __name__ == "__main__":
    corp_name = input("Enter corp name: ")
    ds_token = input("Enter ds token: ")  # Assuming you already have the ds token
    duo_token = input("Enter duo token: ")  # Assuming you already have the duo token
    
    cookies_dict = {"dstoken": ds_token, "_DUO_APER_LOCAL_": duo_token}
    main(corp_name, cookies_dict)

