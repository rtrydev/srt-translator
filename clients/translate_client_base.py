from abc import ABC, abstractmethod
from typing import List

from models.subtitle import Subtitle


class TranslateClientBase(ABC):
    @abstractmethod
    def translate(self, subtitles: List[Subtitle]) -> List[Subtitle]:
        pass
