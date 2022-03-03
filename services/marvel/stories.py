from .requester import Requester


class Stories:
    def __init__(self, request: Requester):
        self.r = request
        self.base_url = "stories"

    def all(self, **kwargs):
        return self.r.request(self.base_url, **kwargs)

    def get(self, story_id, **kwargs):
        return self.r.request(self.base_url, story_id, **kwargs)

    def comics(self, story_id, **kwargs):
        return self.r.request(self.base_url, story_id, "comics", **kwargs)

    def creators(self, story_id, **kwargs):
        return self.r.request(self.base_url, story_id, "creators", **kwargs)

    def events(self, story_id, **kwargs):
        return self.r.request(self.base_url, story_id, "events", **kwargs)

    def series(self, story_id, **kwargs):
        return self.r.request(self.base_url, story_id, "series", **kwargs)

    def characters(self, story_id, **kwargs):
        return self.r.request(self.base_url, story_id, "characters", **kwargs)
