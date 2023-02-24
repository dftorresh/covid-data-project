import requests


def get_configs_from_file(configs_file_path):
    resources_details = {}
    for line in open(configs_file_path):
        key, value = line.rstrip('\n').split(' = ')
        resources_details[key] = value[1:-1]
    return resources_details


def download_file(web_file_url, target_folder):
    r = requests.get(web_file_url, stream=True)
    with open(target_folder, "wb") as file:
        for chunk in r.iter_content(chunk_size=1024):
            # writing one chunk at a time to the file
            if chunk:
                file.write(chunk)
