from src.implemented import youtube, printj


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id

    def print_info(self) -> None:
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        printj(channel)