import json

class ChobbyConfig(object):
    def __init__(self):
        json_data = None
        with open('config.json') as data_file:
        	json_data = json.load(data_file)

        self.auto_download = json_data["auto_download"]
        self.auto_start = json_data["auto_start"]
        self.game_title = json_data["game_title"]

        self.game_rapid = json_data["game_rapid"]
        self.lobby_rapid = json_data["lobby_rapid"]
