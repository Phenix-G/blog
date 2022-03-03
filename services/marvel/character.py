from .requester import Requester


class Characters:
    def __init__(self, request: Requester):
        self.r = request
        self.base_url = "characters"

    def all(self, **kwargs):
        return self.r.request(self.base_url, **kwargs)

    def get(self, character_id, **kwargs):
        return self.r.request(self.base_url, character_id, **kwargs)

    def comics(self, character_id, **kwargs):
        return self.r.request(self.base_url, character_id, "comics", **kwargs)

    def events(self, character_id, **kwargs):
        return self.r.request(self.base_url, character_id, "events", **kwargs)

    def series(self, character_id, **kwargs):
        return self.r.request(self.base_url, character_id, "series", **kwargs)

    def stories(self, character_id, **kwargs):
        return self.r.request(self.base_url, character_id, "stories", **kwargs)
