import os
import json

# Checking if the data folder doesn't exist, and if so, make it.
def check_data_folder(cogname):
    folder = os.path.join('data', cogname)
    if not os.path.exists(folder):
        os.mkdir(folder)
        return False
    return True

# To be honest, most of the code below comes from Red-DiscordBot's dataIO.py

# Load the json file.
def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return save_json(filename, {})
    except json.decoder.JSONDecodeError:
        print('An error occured while trying to load {}.'.format(filename))
        return

def save_json(filename, data):
    path, ext = os.path.splitext(filename)
    temp = '{}_temp.tmp'.format(path)
    with open(temp, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)
    try:
        load_json(temp)
    except json.decoder.JSONDecodeError:
        print('An error occured while trying to save {}.'.format(filename))
        return
    os.replace(temp, filename)
    return data