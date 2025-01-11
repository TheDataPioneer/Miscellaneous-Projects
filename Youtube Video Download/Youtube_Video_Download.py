"""=============================================================================
Filename: Download_Youtube_Video.py
Last updated: 2024-12-07

Script to download videos from YouTube using yt-dlp and store them in a 
user-specified directory.

Inputs:
  - URL of the YouTube video (hard-coded or prompted in the main section)
  - Download directory path (hard-coded or prompted in the main section)
  - Path to cookies.txt file for restricted video access

Outputs:
  - Downloaded video file (in the specified directory)

Requirements:
  - Python 3.6+
  - yt-dlp (install via: pip install yt-dlp)
  - script_logger module (providing the log_message() function)
  - cookies.txt exporter extension (for firefox or chrome)

Description:
  This script extracts metadata from the specified YouTube video using yt-dlp
  without downloading. If metadata extraction is successful, it proceeds to 
  download the video. The script uses a custom logging function (log_message)
  instead of standard prints/logging. It includes:
  
  - Automatic extraction of metadata before downloading.
  - Configurable output folder specified at runtime in the __main__ section.
  - Handles restricted videos using a provided cookies.txt file.

How to Export Cookies Using a Browser Extension

    Install the Extension:
        For Chrome or Edge:
            Install the Get cookies.txt extension.
        For Firefox:
            Install the cookies.txt exporter extension.

    Export the Cookies:
        Open the YouTube website in your browser and log into your account.
        Click the extension icon in your browser toolbar.
        Export cookies for the current tab (YouTube) and save them as a cookies.txt file.
        Choose a location to save the cookies.txt file (e.g., the same directory as your script or another accessible location).

    Verify the Cookies File:
        Open the cookies.txt file in a text editor.
        Check that it contains lines of text, including entries for YouTube, such as youtube.com.
============================================================================="""

# ----------------------------------------------------------------------
# INITIALIZATION
# ----------------------------------------------------------------------
from script_logger import log_message
import os
from yt_dlp import YoutubeDL

# ----------------------------------------------------------------------
# FUNCTIONS
# ----------------------------------------------------------------------

def extract_metadata(url: str, cookie_file: str = None) -> dict:
    """
    Extract metadata for a given YouTube URL without downloading.
    
    Parameters:
        url (str): The YouTube video URL.
        cookie_file (str): Path to the cookies.txt file (optional).
    
    Returns:
        dict: A dictionary of metadata information extracted by yt-dlp. 
              None if extraction fails.
    """
    meta_opts = {'quiet': True, 'ignoreerrors': True}
    
    if cookie_file:
        meta_opts['cookiefile'] = cookie_file
        log_message(f"Using cookie file for metadata extraction: {cookie_file}", type="info")
    
    try:
        with YoutubeDL(meta_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info:
                log_message(f"Metadata extracted successfully for URL: {url}", type="info")
                return info
            else:
                log_message(f"No metadata returned for URL: {url}. Possibly invalid or restricted.", type="error")
                return None
    except Exception as e:
        log_message(f"Failed to extract metadata for {url}. Error: {e}", type="error")
        return None


def download_video(url: str, download_dir: str, cookie_file: str = None) -> bool:
    """
    Download a YouTube video using yt_dlp.
    
    Parameters:
        url (str): The YouTube video URL.
        download_dir (str): The directory where the video will be downloaded.
        cookie_file (str): Path to the cookies.txt file (optional).
    
    Returns:
        bool: True if the download was successful, False otherwise.
    """
    info = extract_metadata(url, cookie_file)
    if not info:
        log_message(f"Could not extract metadata for {url}. Skipping download.", type="error")
        return False

    title = info.get('title', 'Unknown Title')
    uploader = info.get('uploader', 'Unknown Uploader')
    duration = info.get('duration', 0)

    log_message(f"Preparing to download: {title}", type="info")
    log_message(f"Uploader: {uploader}", type="info")
    log_message(f"Duration: {duration} seconds", type="info")

    os.makedirs(download_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'ignoreerrors': True,
    }

    if cookie_file:
        ydl_opts['cookiefile'] = cookie_file
        log_message(f"Using cookie file: {cookie_file}", type="info")
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        log_message(f"Download completed: {title}", type="info")
        return True
    except Exception as e:
        log_message(f"Download failed for {url}. Error: {e}", type="critical")
        return False


# ----------------------------------------------------------------------
# MAIN EXECUTION
# ----------------------------------------------------------------------

if __name__ == "__main__":
    # Input variables
    video_url = "https://www.youtube.com/watch?v=admjE_WT0og"
    download_dir = r"C:\Users\Joshu\Videos"
    cookie_file = r"C:\Users\Joshu\OneDrive\Documents\cookies.txt"  

    # Ensure the cookie file exists
    if not os.path.isfile(cookie_file):
        log_message(f"Cookie file not found: {cookie_file}", type="critical")
        exit(1)

    # Start the download process
    log_message(f"Starting download process for URL: {video_url}", type="info")
    success = download_video(video_url, download_dir, cookie_file)

    if success:
        log_message("The video was downloaded successfully.", type="info")
    else:
        log_message("The video could not be downloaded.", type="warning")
