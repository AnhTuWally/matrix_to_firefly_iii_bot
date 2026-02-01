import json

class ConfigReader:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config_data = self._load_config()

    def _load_config(self):
        """Load the JSON configuration file."""
        try:
            with open(self.config_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"Configuration file {self.config_file} not found.")
        except json.JSONDecodeError as e:
            raise Exception(f"Error parsing JSON file: {e}")

    def get(self, *keys):
        """Retrieve a value from the configuration using a sequence of keys."""
        data = self.config_data
        for key in keys:
            if key in data:
                data = data[key]
            else:
                raise KeyError(f"Key {' -> '.join(keys)} not found in configuration.")
        return data
