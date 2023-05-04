
import json
class User:
    def __init__(self):
        self.player_id = ""
        self.name = ""

    def addPlayer(self, player_id, name):
        self.player_id = player_id
        self.name = name

    def __str__(self):
        """String version of this objects state"""
        attributes = {}
        attributes["userId"] = self.player_id
        attributes["name"] = self.name
        return json.dumps(attributes)
