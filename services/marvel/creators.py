from .requester import Requester


class Creators:
    def __init__(self, request: Requester):
        self.r = request
        self.base_url = "creators"

    def all(self, **kwargs):
        return self.r.request(self.base_url, **kwargs)

    def get(self, creator_id, **kwargs):
        return self.r.request(self.base_url, creator_id, **kwargs)

    def comics(self, creator_id, **kwargs):
        return self.r.request(self.base_url, creator_id, "comics", **kwargs)

    def events(self, creator_id, **kwargs):
        return self.r.request(self.base_url, creator_id, "events", **kwargs)

    def stories(self, creator_id, **kwargs):
        return self.r.request(self.base_url, creator_id, "stories", **kwargs)

    def series(self, creator_id, **kwargs):
        return self.r.request(self.base_url, creator_id, "series", **kwargs)
