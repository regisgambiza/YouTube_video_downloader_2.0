import sys
import time
from venv import logger
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMessageBox, QTableWidgetItem, QTableWidget, QHeaderView
from PyQt5.uic import loadUi
from pytube import YouTube, Playlist
from download_thread import DownloadThread
from add_url_thread import AddUrlThread


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Load the main GUI
        self.download_thread = None
        loadUi('app/ui/main_window_2.0.ui', self)
        self.progressBar.setValue(0)

        # Customise the table widget
        self.tableWidget.setShowGrid(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)

        self.progressBar.setVisible(False)

        # Load the stylesheet
        # self.stylesheet = "app/resources/css/style.qss"
        try:
            with open(self.stylesheet) as f:
                style = f.read()
                self.setStyleSheet(style)
        except FileNotFoundError:
            print("Stylesheet file not found")
        except Exception as e:
            print(f"Error loading stylesheet: {str(e)}")

        # Load icons for push buttons
        self.downloadOptionsButton.setIcon(QIcon('assets/settings-svgrepo-com.svg'))
        self.addUrlButton.setIcon(QIcon('assets/add-file-svgrepo-com.svg'))
        self.downloadAllButton.setIcon(QIcon('assets/download.svg'))
        self.pushButton.setIcon(QIcon("assets/stop-svgrepo-com.svg"))

        # Variables
        self.download_queue = []

        # Connect push buttons to functions
        self.downloadOptionsButton.clicked.connect(self.show_options_dialog)
        self.addUrlButton.clicked.connect(self.add_url)
        self.downloadAllButton.clicked.connect(self.download_media)


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
            playlist = Playlist(url)
            url_list = playlist.video_urls
        else:
            url_list = [url]

        # Start a separate thread to add URLs to the download queue
        self.add_url_thread = AddUrlThread(url_list)
        self.add_url_thread.progress_signal.connect(self.handle_add_url_progress)
        self.add_url_thread.finished.connect(self.cleanup_add_url_thread)
        self.add_url_thread.start()

    def handle_add_url_progress(self, new_video):
        """Handle progress signals emitted by the AddUrlThread."""
        if new_video:
            self.download_queue.append(new_video)
            self.display_videos_on_table()

    def cleanup_add_url_thread(self):
        """Clean up the AddUrlThread."""
        self.add_url_thread.progress_signal.disconnect(self.handle_add_url_progress)
        self.add_url_thread.finished.disconnect(self.cleanup_add_url_thread)
        self.add_url_thread.deleteLater()

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
        table_widget.setColumnCount(4)  # Assuming you want to display four columns

        # Get the current row count to append new rows
        current_row_count = table_widget.rowCount()

        # Set the number of columns and column headers if not already set
        if table_widget.columnCount() == 0:
            table_widget.setColumnCount(4)  # Assuming you want to display four columns
            table_widget.setHorizontalHeaderLabels(["Video Title", "Status", "Video Size", "Progress"])

        # Populate the table with YouTubeVideo objects
        for row, video in enumerate(self.download_queue, start=current_row_count):
            table_widget.insertRow(row)
            table_widget.setItem(row, 0, QTableWidgetItem(video.video_title))
            table_widget.setItem(row, 1, QTableWidgetItem("Queued"))
            table_widget.setItem(row, 2, QTableWidgetItem(video.video_size))
            table_widget.setItem(row, 3, QTableWidgetItem("---"))
            self.align_text_for_table_widget()

    def update_progress(self, progress, status):
        # Update cell content
        print(f"Percentage:{progress}")
        self.progressBar.setVisible(True)
        self.progressBar.setValue(progress)
        self.tableWidget.setItem(0, 3, QTableWidgetItem(str(progress) + "%"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(status))
        self.align_text_for_table_widget()


    def align_text_for_table_widget(self):
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.item(i, 1).setTextAlignment(Qt.AlignCenter)
            self.tableWidget.item(i, 2).setTextAlignment(Qt.AlignCenter)
            self.tableWidget.item(i, 3).setTextAlignment(Qt.AlignCenter)

    def download_media(self):
        if not self.download_queue:
            return  # No videos in the queue
        self.downloadAllButton.setEnabled(False)

        video = self.download_queue[0]
        url = video.video_url

        # Start a new thread for the current video
        self.download_thread = DownloadThread(url)
        self.download_thread.progress_changed.connect(self.update_progress)

        # Connect the finished signal to the download_next_video method
        self.download_thread.finished.connect(self.download_next_video)

        # Start the thread
        self.download_thread.start()

    def download_next_video(self):
        # Disconnect the finished signal to avoid calling download_next_video multiple times
        self.download_thread.finished.disconnect(self.download_next_video)

        # Remove video from first position
        self.download_queue.pop(0)
        self.display_videos_on_table()

        # Check if there are more videos in the queue
        if self.download_queue:
            # Download the next video after a short delay to allow the thread to finish
            QTimer.singleShot(100, self.download_media)
        self.downloadAllButton.setEnabled(True)


class YouTubeVideo:
    def __init__(self, video_url, _video_title, video_size):
        self.video_url = video_url
        self.video_title = _video_title
        self.video_size = video_size

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
