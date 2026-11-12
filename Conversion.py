import os
import subprocess
import yt_dlp as youtube_dl
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

def ensure_absolute_path(path):
    """Convert a relative path to an absolute path."""
    return os.path.abspath(path)

def ensure_directory_exists(directory_path):
    """Ensure the specified directory exists, or create it."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def upscale_video(input_path, output_path, resolution="1280:720", method="bicubic"): #bicubic
    """
    Upscales a video to the specified resolution using FFmpeg.

    :param input_path: Path to the input video file.
    :param output_path: Path to save the upscaled video.
    :param resolution: Target resolution (default is 1280x720).
    :param method: Scaling method ('bicubic', 'lanczos', etc.).
    """
    input_path = ensure_absolute_path(input_path)
    output_path = ensure_absolute_path(output_path)

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file '{input_path}' does not exist.")

    print(f"DEBUG: Input Path = {input_path}")
    print(f"DEBUG: Output Path = {output_path}")

    command = [
        "ffmpeg",
        "-y",  # Force overwrite without prompt
        "-i", input_path,
        "-vf", f"scale={resolution}:flags={method}",
        output_path
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg Error:\n{result.stderr}")
        raise Exception("Upscaling failed.")

    print(f"Upscaled video saved to: {output_path}")

def download_video(video_link, download_path):
    """
    Downloads a video from a YouTube link using yt-dlp.

    :param video_link: YouTube video link.
    :param download_path: Path to save the downloaded video.
    :return: Path to the downloaded video.
    """
    ensure_directory_exists(download_path)  # Ensure download directory exists

    download_path = ensure_absolute_path(download_path)

    try:
        custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'user_agent': custom_user_agent,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_link, download=True)
            downloaded_file = ydl.prepare_filename(info_dict)
            downloaded_file = ensure_absolute_path(downloaded_file)  # Ensure file path is absolute
            print(f"DEBUG: Downloaded video to: {downloaded_file}")
            return downloaded_file

    except Exception as e:
        raise Exception(f"Error while downloading video: {e}")

# Specify paths
video_link = "https://www.youtube.com/watch?v=ik4Rn3bWrcs&t=69s"
# Set the Google Drive folder path to save the video
google_drive_path = "/content/drive/My Drive/ColabVideos"
download_path = google_drive_path
output_path = os.path.join(download_path, "upscaled_video.mp4")  # Output path for the upscaled video

# Ensure the Google Drive folder exists
ensure_directory_exists(google_drive_path)

try:
    print("Processing video...")
    input_path = download_video(video_link, download_path)
    upscale_video(input_path, output_path)

except Exception as e:
    print(f"Error: {e}")
