from .base import Base
from .character import Characters
from .comics import Comics
from .creators import Creators
from .events import Events
from .series import Series
from .stories import Stories


class Marvel(Base):
    def __init__(self, private_key, public_key):
        super().__init__(private_key, public_key)
        self.characters = Characters(self.r)
        self.events = Events(self.r)
        self.series = Series(self.r)
        self.comics = Comics(self.r)
        self.creators = Creators(self.r)
        self.stories = Stories(self.r)
