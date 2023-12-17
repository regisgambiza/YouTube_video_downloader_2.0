import sys
from venv import logger
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QWidget, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from pytube import YouTube, Playlist


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Load the main GUI
        loadUi('app/ui/main_window_2.0.ui', self)

        # Load the stylesheet
        # self.stylesheet = "/Users/regisgambiza/PycharmProjects/Youtub_dwnloder/src/app/css/apple_look.qss"
        try:
            with open(self.stylesheet) as f:
                style = f.read()
                self.setStyleSheet(style)
        except FileNotFoundError:
            print("Stylesheet file not found")
        except Exception as e:
            print(f"Error loading stylesheet: {str(e)}")

        # Connect push buttons to functions
        self.downloadOptionsButton.clicked.connect(self.show_options_dialog)
        self.addUrlButton.clicked.connect(self.add_url)

        # Variables
        self.download_queue = []

    def show_options_dialog(self):
        """Displays the settings dialog"""
        options_dialog = DownloadOptionsDialog(self)
        options_dialog.exec_()

    def add_url(self):
        """Adds a video URL or playlist URL to the download queue."""

        url = self.lineEdit.text()
        self.lineEdit.clear()
        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a valid YouTube URL or playlist URL.")
            return

        if "playlist" in url.lower():
            QMessageBox.warning(self, "Warning", "Please wait while videos are added to the download queue!")
            try:
                playlist = Playlist(url)
                for video_url in playlist.video_urls:
                    self._add_video(video_url)
                    self.display_videos_on_table()
            except Exception as e:
                logger.error(f"Error adding playlist '{url}': {e}")
        else:
            try:
                self._add_video(url)
                self.display_videos_on_table()
            except Exception as e:
                logger.error(f"Error adding video '{url}': {e}")



    def _add_video(self, url: str):
        """Adds a single video to the download queue."""

        global video_title
        try:
            yt = YouTube(url)
            video = yt.streams.filter(file_extension="mp4").get_highest_resolution()
            video_title = video.title
            video_size = self.get_size_str(video.filesize)
            new_video = YouTubeVideo(url, video_title, video_size)
            self.download_queue.append(new_video)

        except Exception as e:
            logger.error(f"Error adding video '{video_title}': {e}")
        print(len(self.download_queue))


    def get_size_str(self, size_in_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_in_bytes < 1024.0:
                break
            size_in_bytes /= 1024.0
        return "{:.2f} {}".format(size_in_bytes, unit)

    def display_videos_on_table(self):
        """Display all videos in the download queue on QTableWidget."""

        # Assuming you have a QTableWidget named 'tableWidget' in your UI
        table_widget = self.tableWidget

        # Clear existing contents from the table
        table_widget.setRowCount(0)
        table_widget.setColumnCount(5)  # Assuming you want to display three columns

        # Get the current row count to append new rows
        current_row_count = table_widget.rowCount()

        # Set the number of columns and column headers if not already set
        if table_widget.columnCount() == 0:
            table_widget.setColumnCount(5)  # Assuming you want to display three columns
            table_widget.setHorizontalHeaderLabels(["Video Title", "Status", "Video Size", "Downloaded", "Progress"])

        # Populate the table with YouTubeVideo objects
        for row, video in enumerate(self.download_queue, start=current_row_count):
            table_widget.insertRow(row)
            table_widget.setItem(row, 0, QTableWidgetItem(video.video_title))
            table_widget.setItem(row, 1, QTableWidgetItem("Queued"))
            table_widget.setItem(row, 2, QTableWidgetItem(video.video_size))
            table_widget.setItem(row, 3, QTableWidgetItem("---"))
            table_widget.setItem(row, 4, QTableWidgetItem("---"))


class YouTubeVideo:
    def __init__(self, video_url, video_title, video_size):
        self.video_url = video_url
        self.video_title = video_title
        self.video_size = video_size

    # Define additional methods as needed

    def __str__(self):
        return f"YouTube video: {self.video_title} ({self.video_size} bytes)"


class DownloadOptionsDialog(QDialog):
    def __init__(self, parent=None):
        super(DownloadOptionsDialog, self).__init__(parent)
        loadUi('app/ui/download_options_dialog.ui', self)

        try:
            with open(self.stylesheet) as f:
                style = f.read()
                self.setStyleSheet(style)
        except FileNotFoundError:
            print("Stylesheet file not found")
        except Exception as e:
            print(f"Error loading stylesheet: {str(e)}")


class DownloadThread(QThread):
    """ Worker thread for handling video and playlist downloads."""
    progress_signal = pyqtSignal(int, str, str)
    completion_signal = pyqtSignal(str)
    stop_signal = pyqtSignal()

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        self.download_video()

    def download_video(self):
        yt = YouTube(self.url, on_progress_callback=self.on_progress)
        video_streams = yt.streams.filter(file_extension="mp4")
        selected_video_stream = video_streams.get_highest_resolution()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
