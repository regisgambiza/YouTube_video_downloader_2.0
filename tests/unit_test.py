import sys
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from main import MainWindow


class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()

    def tearDown(self):
        self.window.close()

    def test_add_url_single_video(self):
        # Simulate adding a valid YouTube video URL
        url = "https://www.youtube.com/watch?v=T_KrYLW4jw8&list=PLzMcBGfZo4-nyLTlSRBvo0zjSnCnqjHYQ&index=1&pp=iAQB"
        self.window.lineEdit.setText(url)
        QTest.mouseClick(self.window.addUrlButton, Qt.LeftButton)

        # Check if the video is added to the download queue
        self.assertEqual(len(self.window.download_queue), 1)
        self.assertEqual(self.window.download_queue[0].video_url, url)

    def test_add_url_playlist(self):
        # Simulate adding a valid YouTube playlist URL
        playlist_url = "https://youtube.com/playlist?list=PLzMcBGfZo4-nyLTlSRBvo0zjSnCnqjHYQ&si=cr0i6dYo3GLhZvOL"
        self.window.lineEdit.setText(playlist_url)
        QTest.mouseClick(self.window.addUrlButton, Qt.LeftButton)

        # Check if videos from the playlist are added to the download queue
        self.assertNotEqual(len(self.window.download_queue), 0)
        for video in self.window.download_queue:
            self.assertTrue(video.video_url.startswith("https://www.youtube.com/watch?v="))

    def test_download_media(self):
        # Add a video to the download queue
        url = "https://www.youtube.com/watch?v=your_video_id"
        self.window._add_video(url)

        # Simulate clicking the "Download All" button
        QTest.mouseClick(self.window.downloadAllButton, Qt.LeftButton)

        # Check if the download thread is started and the video is removed from the queue
        self.assertIsNotNone(self.window.download_thread)
        self.assertEqual(len(self.window.download_queue), 0)


if __name__ == '__main__':
    unittest.main()
