import json
import pkgutil

class LauncherConfig(object):
    def __init__(self):
        configFile = None
        try:
            configFile = pkgutil.get_data("spring_launcher", "config.json")
        except:
            pass
        if configFile:
            configFile = configFile.decode('utf-8')
        else:
            configFile = open("config.json", "r").read()
        json_data = json.loads(configFile)

        local_connection = {
            "host": None,
            "port": None
        }
        try:
            local_connection["host"] = json_data["local_connection"]["host"]
            local_connection["port"] = json_data["local_connection"]["port"]
            self.local_connection = local_connection
        except:
            self.local_connection = None

        self.auto_download = json_data["auto_download"]
        self.auto_start = json_data["auto_start"]
        self.no_downloads = json_data["no_downloads"]

        self.game_title = json_data["game_title"]

        self.launcher_game_id = json_data["launcher_game_id"]

        self.games = json_data.get("games", [])
        self.maps = json_data.get("maps", [])
        self.engines = json_data.get("engines", [])

        self.start_args = json_data.get("start_args")
