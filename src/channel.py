import json
from typing import Any

from src.implemented import youtube, printj


class Channel:
    """Класс для ютуб-канала"""
    __youtube_api = youtube

    def __init__(self, channel_id: str) -> None:
        self.__channel_id = channel_id
        self._channel = self.__youtube_api.channels().list(id=channel_id, part='snippet,statistics').execute()

        self.title = self._channel["items"][0]["snippet"]["title"]
        self.description = self._channel["items"][0]["snippet"]["description"]
        self.url = "https://www.youtube.com/" + self._channel["items"][0]["snippet"]["customUrl"]
        self.subscribers = int(self._channel["items"][0]["statistics"]["subscriberCount"])
        self.video_count = self._channel["items"][0]["statistics"]["videoCount"]
        self.views = self._channel["items"][0]["statistics"]["viewCount"]

    def __str__(self) -> str:
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subscribers + other.subscribers

    def __sub__(self, other):
        return self.subscribers - other.subscribers

    def __lt__(self, other):
        return self.subscribers < other.subscribers

    def __le__(self, other):
        return self.subscribers <= other.subscribers

    def __gt__(self, other):
        return self.subscribers > other.subscribers

    def __ge__(self, other):
        return self.subscribers >= other.subscribers

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    def print_info(self) -> None:
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        printj(channel)

    @classmethod
    def get_service(cls) -> Any:
        return cls.__youtube_api

    def to_json(self, file) -> None:
        channel_data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers": self.subscribers,
            "video_count": self.video_count,
            "views": self.views
        }
        with open(file, 'w', encoding='utf-8') as json_file:
            json.dump(channel_data, json_file, ensure_ascii=False, indent=4)


