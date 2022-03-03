from .requester import Requester


class Comics:
    def __init__(self, request: Requester):
        self.r = request
        self.base_url = "comics"

    def all(self, **kwargs):
        return self.r.request(self.base_url, **kwargs)

    def get(self, comic_id, **kwargs):
        return self.r.request(self.base_url, comic_id, **kwargs)

    def characters(self, comic_id, **kwargs):
        return self.r.request(self.base_url, comic_id, "characters", **kwargs)

    def events(self, comic_id, **kwargs):
        return self.r.request(self.base_url, comic_id, "events", **kwargs)

    def stories(self, comic_id, **kwargs):
        return self.r.request(self.base_url, comic_id, "stories", **kwargs)
