from .base import Base
from .character import Characters


class Marvel(Base):
    def __init__(self, private_key, public_key):
        super().__init__(private_key, public_key)
        self.characters = Characters(self.r)
        self.events = "events"
        self.series = "series"
        self.comics = "comics"
        self.creators = "creators"
        self.stories = "stories"
