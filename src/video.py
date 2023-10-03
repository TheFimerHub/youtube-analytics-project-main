import json
from src.implemented import youtube, printj


class Video():
    def __init__(self, video_id):
        self.__video_id = video_id
        self._video = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id).execute()
        self.title = self._video['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/video/{self.__video_id}"
        self.view_count = self._video['items'][0]['statistics']['viewCount']
        self.like_count = self._video['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.title}'

    @property
    def video_id(self) -> str:
        return self.__video_id

    def print_info(self) -> None:
        printj(self._video)

    def to_json(self, file) -> None:
        video_data = {
            "video_id": self.video_id,
            "title": self.title,
            "url": self.url,
            "view_count": self.view_count,
            "like_count": self.like_count
        }
        with open(file, 'w', encoding='utf-8') as json_file:
            json.dump(video_data, json_file, ensure_ascii=False, indent=4)


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    def get_playlist_id(self):
        return self.__playlist_id

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.video_id}', '{self.get_playlist_id()}', '{self.title}', '{self.url}', {self.view_count}, {self.like_count})"
