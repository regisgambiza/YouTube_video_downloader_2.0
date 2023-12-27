from PyQt5.QtCore import pyqtSignal, QThread
from pytube import YouTube

class DownloadThread(QThread):
    progress_changed = pyqtSignal(int, str)
    finished = pyqtSignal(str, bool)

    def __init__(self, video_url):
        super().__init__()
        self.video_url = video_url

    def run(self):
        print("Run started")
        self.download_video()
        self.finished.emit("Download completed", True)

    def download_video(self):
        """Download a single video."""
        try:
            yt = YouTube(self.video_url, on_progress_callback=self.on_progress)
            video_streams = yt.streams.filter(file_extension="mp4")
            selected_video_stream = video_streams.get_highest_resolution()
            self.progress_changed.emit(0, f"Downloading")

            # Download the video
            selected_video_stream.download(output_path="Downloads/")
        except Exception as e:
            self.finished.emit(f"Download failed: {str(e)}", False)

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = int(bytes_downloaded / total_size * 100)
        self.progress_changed.emit(percentage, "Downloading")
