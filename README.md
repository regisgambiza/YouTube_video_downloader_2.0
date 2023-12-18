# YouTube Video Downloader App

## Overview

The **YouTube Video Downloader app** is a simple desktop application built in Python using PyQt5 for the graphical user interface and Pytube for interacting with the YouTube API. This application allows users to download both single videos and entire playlists from YouTube seamlessly.

## Features

- **Download Single Videos:** Enter the URL of a YouTube video, and the app will download it for you.
  
- **Download Playlists:** Paste the URL of a YouTube playlist, and the app will prompt you for confirmation before downloading the entire playlist.

- **User-friendly Interface:** The app provides a clean and intuitive user interface, making it easy for users to interact with and initiate downloads.

- **Real-time Progress Updates:** Track the progress of your downloads with real-time updates on the application window. The progress bar shows the completion percentage, and the text browser provides additional information, including the video name and download size.

- **Error Handling:** The application gracefully handles errors during the download process, providing informative messages to the user in case of issues.

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python (version 3.6 or higher)**
- **PyQt5 library**
- **Pytube library**

# TODO List

## 1. Confirmation message before stopping downloads:

- [ ] Add a "Stop Download" button to the UI.
- [ ] When the button is clicked, show a confirmation message box asking the user to confirm stopping the download.
- [ ] If the user confirms, call the stop method of the DownloadThread to stop the download.

## 2. Options for choosing resolutions or download formats:

- [ ] Add a dropdown menu or radio buttons to the UI where the user can choose the desired video resolution or download format (e.g., MP4, MP3).
- [ ] When the user selects a different option, dynamically update the information displayed in the UI, such as estimated download size.
- [ ] Pass the selected option to the DownloadThread to download the video in the chosen format or resolution.

## 3. Queue system for multiple downloads:

- [ ] Implement a queue data structure to store download URLs in a specific order.
- [ ] Allow the user to add multiple URLs to the queue and specify the order they want them to be downloaded in.
- [ ] Start downloading the first URL in the queue and then proceed to the next one after completion or error.
- [ ] Display the download queue in the UI and provide options for adding, removing, and rearranging URLs.

## 4. Searching for videos, displaying video information, and managing completed downloads:

- [ ] Add a search bar to the UI where the user can enter keywords to search for videos on YouTube.
- [ ] Use the YouTube Data API to retrieve video information such as title, description, thumbnail image, and available resolutions.
- [ ] Display the retrieved information in a dedicated area of the UI.
- [ ] Implement a "Downloads" section in the UI where the user can see a list of completed downloads, including video title, download date, and file location.
- [ ] Allow the user to open the downloaded files, delete them from the list, or clear the entire history.

## 5. UI design and responsiveness:

- [ ] Enhance the UI design by incorporating modern elements and using a consistent style throughout the application.
- [ ] Leverage layout managers like QGridLayout for better responsiveness and adaptability to different screen sizes.
- [ ] Ensure that the UI elements are properly aligned and spaced to provide a visually appealing and user-friendly experience.

## 6. Comments and unit tests:

- [ ] Add comprehensive comments throughout the code to explain complex logic, functionalities, and variable names.
- [ ] Implement unit tests using frameworks like Pytest or unittest to ensure the functionality of different parts of the application and prevent regressions during future development.

**Note:** Integrating all of these features will require extensive coding and design work. It is recommended to prioritize and implement them in stages, starting with the most critical ones. This will allow for easier testing and debugging while also delivering valuable functionality to users in a timely manner.



