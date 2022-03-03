from .requester import Requester


class Events:
    def __init__(self, request: Requester):
        self.r = request
        self.base_url = "events"

    def all(self, **kwargs):
        return self.r.request(self.base_url, **kwargs)

    def get(self, event_id, **kwargs):
        return self.r.request(self.base_url, event_id, **kwargs)

    def comics(self, event_id, **kwargs):
        return self.r.request(self.base_url, event_id, "comics", **kwargs)

    def creators(self, event_id, **kwargs):
        return self.r.request(self.base_url, event_id, "creators", **kwargs)

    def stories(self, event_id, **kwargs):
        return self.r.request(self.base_url, event_id, "stories", **kwargs)

    def series(self, event_id, **kwargs):
        return self.r.request(self.base_url, event_id, "series", **kwargs)

    def characters(self, event_id, **kwargs):
        return self.r.request(self.base_url, event_id, "characters", **kwargs)
