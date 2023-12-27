from PyQt5.QtCore import QThread, pyqtSignal
from pytube import Playlist, YouTube
from main import YouTubeVideo  # Import the YouTubeVideo class from your main file

class AddUrlThread(QThread):
    progress_signal = pyqtSignal(YouTubeVideo)

    def __init__(self, url_list):
        super(AddUrlThread, self).__init__()
        self.url_list = url_list

    def run(self):
        for url in self.url_list:
            new_video = self.add_url_to_queue(url)
            if new_video:
                self.progress_signal.emit(new_video)
            self.sleep(2)  # You can adjust the sleep duration as needed

        # Add a cleanup step
        self.quit()
        self.wait()

    def add_url_to_queue(self, url):
        try:
            yt = YouTube(url)
            video = yt.streams.filter(file_extension="mp4").get_highest_resolution()
            video_title = video.title
            video_size = self.get_size_str(video.filesize)
            new_video = YouTubeVideo(url, video_title, video_size)
            self.sleep(2)
            return new_video
        except Exception as e:
            self.progress_signal.emit(None)
            return None

    def get_size_str(self, size_in_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_in_bytes < 1024.0:
                break
            size_in_bytes /= 1024.0
        return "{:.2f} {}".format(size_in_bytes, unit)


