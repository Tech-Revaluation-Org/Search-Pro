# HyperSearch Browser

## Features

- **Multi-Search Capability**: Allows users to perform searches across various categories including Text, Image, File, Audio, Code, AI, Maps, and Trends.
  
- **Custom Search Engines**: Users can add custom search engines for each category, enhancing the flexibility of the search functionality.

- **File Upload Support**: Users can upload files for specific search types (Image, File, Audio), which will be included in the search query.

- **Modern UI Design**: The application features a sleek, modern interface with a dark theme, providing a visually appealing user experience.

- **Tabbed Browsing**: Each search result opens in a new tab, allowing users to easily switch between different search results.

- **Progress Indicator**: A progress bar indicates the loading status of search results, enhancing user feedback during searches.

- **Settings Management**: Users can save and load their preferred search engine settings, ensuring a personalized experience.

- **Context Menu for Settings**: Right-clicking on the settings button opens a context menu for managing search engines, including toggling their active status.

- **Thread Pool for Performance**: Utilizes a thread pool to manage concurrent searches, improving performance and responsiveness.

- **Dynamic UI Updates**: The interface updates dynamically based on user selections, such as showing or hiding the upload button based on the selected search type.

## How It Works

1. **Initialization**: The application initializes the main window, sets up the UI components, and loads user settings from a JSON file.

2. **Search Type Selection**: Users select the type of search they want to perform from a dropdown menu, which dynamically updates the UI to show relevant options.

3. **File Upload**: For applicable search types, users can upload files, which are then included in the search query.

4. **Search Execution**: When the user clicks the search button, the application constructs the search URLs based on the selected search type and active search engines.

5. **Concurrent Searches**: The application launches multiple searches concurrently using a thread pool, allowing for faster results.

6. **Result Display**: Each search result is displayed in a new tab, with the option to close tabs as needed.

7. **Settings Management**: Users can manage their search engine preferences through a context menu, allowing for a customized search experience.

8. **Progress Tracking**: The application tracks the progress of ongoing searches and updates the UI accordingly, providing feedback to the user.

## Installation

To run the HyperSearch Browser, you need to install the required Python packages. You can do this using `pip`. Here’s how:

1. Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. Install the required packages by running the following command in your terminal or command prompt:

   ```bash
   pip install PyQt6 PyQt6-WebEngine
