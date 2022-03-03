from .requester import Requester


class Base:
    def __init__(self, private_key, public_key):
        self.r = Requester(private_key, public_key)
