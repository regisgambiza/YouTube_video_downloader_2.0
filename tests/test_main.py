import sys
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from main_2 import MainWindow, DownloadOptionsDialog


class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()

    def test_initialization(self):
        self.assertIsNotNone(self.main_window)
        self.assertIsInstance(self.main_window, MainWindow)
        self.assertEqual(len(self.main_window.download_queue), 0)

    def test_add_url(self):
        # Simulate adding a URL to the QLineEdit
        url = "https://www.youtube.com/watch?v=prmqgY3ZBaM&list=PLSxDqKASb3v7t4x3EBGp6tUATrShwDpmd&index=1&pp=iAQB"
        self.main_window.lineEdit.setText(url)

        # Trigger the add_url method
        QTest.mouseClick(self.main_window.addUrlButton, Qt.LeftButton)

        # Verify that the download_queue has been updated
        self.assertEqual(len(self.main_window.download_queue), 1)
        self.assertEqual(self.main_window.download_queue[0].video_url, url)

    def test_display_videos_on_table(self):
        # Simulate adding a video to the download queue
        url = "https://www.youtube.com/watch?v=prmqgY3ZBaM&list=PLSxDqKASb3v7t4x3EBGp6tUATrShwDpmd&index=1&pp=iAQB"
        video = self.main_window._add_video(url)

        # Trigger the display_videos_on_table method
        self.main_window.display_videos_on_table()

        # Verify that the table widget has been updated
        self.assertEqual(self.main_window.tableWidget.rowCount(), 1)
        self.assertEqual(self.main_window.tableWidget.item(0, 0).text(), video.video_title)

    def test_download_media(self):
        # Simulate adding a video to the download queue
        url = "https://www.youtube.com/watch?v=prmqgY3ZBaM&list=PLSxDqKASb3v7t4x3EBGp6tUATrShwDpmd&index=1&pp=iAQB"
        self.main_window._add_video(url)

        # Trigger the download_media method
        self.main_window.download_media()

        # Verify that the download_thread has started
        self.assertIsNotNone(self.main_window.download_thread)

    def tearDown(self):
        del self.main_window
        del self.app


class TestDownloadOptionsDialog(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.options_dialog = DownloadOptionsDialog()

    def test_initialization(self):
        self.assertIsNotNone(self.options_dialog)
        self.assertIsInstance(self.options_dialog, DownloadOptionsDialog)

    def tearDown(self):
        del self.options_dialog
        del self.app


if __name__ == '__main__':
    unittest.main()
