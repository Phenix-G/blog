from .requester import Requester


class Series:
    def __init__(self, request: Requester):
        self.r = request
        self.base_url = "series"

    def all(self, **kwargs):
        return self.r.request(self.base_url, **kwargs)

    def get(self, series_id, **kwargs):
        return self.r.request(self.base_url, series_id, **kwargs)

    def comics(self, series_id, **kwargs):
        return self.r.request(self.base_url, series_id, "comics", **kwargs)

    def creators(self, series_id, **kwargs):
        return self.r.request(self.base_url, series_id, "creators", **kwargs)

    def stories(self, series_id, **kwargs):
        return self.r.request(self.base_url, series_id, "stories", **kwargs)

    def events(self, series_id, **kwargs):
        return self.r.request(self.base_url, series_id, "events", **kwargs)

    def characters(self, series_id, **kwargs):
        return self.r.request(self.base_url, series_id, "characters", **kwargs)
