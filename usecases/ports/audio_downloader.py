from abc import ABC, abstractmethod
from domain.video import Video


class AudioDownloader(ABC):
    @abstractmethod
    def execute(self, video: Video):
        pass
