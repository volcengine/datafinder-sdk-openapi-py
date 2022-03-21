import json


class JSONFormatter:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
