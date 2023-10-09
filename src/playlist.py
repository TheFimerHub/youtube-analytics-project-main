import datetime
from src.implemented import youtube

class PlayList:
    def __init__(self, playlist_id):
        """
        Инициализирует объект PlayList с заданным идентификатором плейлиста.
        :param playlist_id: Идентификатор плейлиста на YouTube.
        """
        self.__playlist_id = playlist_id
        self._playlist = youtube.playlists().list(part='snippet', id=playlist_id).execute()
        self.title = self._playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"

    @property
    def total_duration(self):
        """
        Возвращает общую продолжительность видеороликов в плейлисте.
        :return: Общая продолжительность видеороликов в виде объекта datetime.timedelta.
        """
        playlist_items = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=self.__playlist_id,
            maxResults=50
        ).execute()

        total_seconds = 0
        for item in playlist_items['items']:
            video_id = item['contentDetails']['videoId']
            video_info = youtube.videos().list(
                part='contentDetails',
                id=video_id
            ).execute()
            video_duration = video_info['items'][0]['contentDetails']['duration']
            parsed_duration = self.transcript_duration(video_duration)
            total_seconds += parsed_duration.total_seconds()

        return datetime.timedelta(seconds=total_seconds)

    @staticmethod
    def transcript_duration(duration_str):
        """
        Преобразует строку продолжительности видеоролика в объект datetime.timedelta.
        :param duration_str: Строка продолжительности видеоролика в формате ISO 8601.
        :return: Продолжительность видеоролика в виде объекта datetime.timedelta.
        """
        duration_str = duration_str.replace("PT", "")

        parts = duration_str.split("M")
        minutes = int(parts[0])

        if "S" in parts[1]:
            seconds = int(parts[1].replace("S", ""))
        else:
            seconds = 0

        return datetime.timedelta(minutes=minutes, seconds=seconds)

    def show_best_video(self):
        """
        Возвращает URL видеоролика с наибольшим количеством лайков в плейлисте.
        :return: URL видеоролика с наибольшим количеством лайков.
        """
        playlist_items = youtube.playlistItems().list(
            part='snippet',
            playlistId=self.__playlist_id,
            maxResults=50
        ).execute()

        best_video_url = ""
        max_likes = 0

        for item in playlist_items['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_info = youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()
            likes = int(video_info['items'][0]['statistics']['likeCount'])
            if likes > max_likes:
                max_likes = likes
                best_video_url = f"https://youtu.be/{video_id}"

        return best_video_url
