import os
from pydub import AudioSegment
from pydub.utils import mediainfo
import sys

# Define the maximum duration in milliseconds (2 minutes and 32 seconds)
MAX_DURATION_MS = 2 * 60 * 1000 + 32 * 1000  # 152,000 ms

# Supported audio formats
SUPPORTED_FORMATS = ('.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac', '.wma')

def trim_audio(file_path, output_path=None, max_duration=MAX_DURATION_MS):
    """
    Trims the audio file to the specified maximum duration.

    :param file_path: Path to the original audio file.
    :param output_path: Path to save the trimmed audio. If None, overwrites the original file.
    :param max_duration: Maximum duration in milliseconds.
    """
    try:
        # Load the audio file
        audio = AudioSegment.from_file(file_path)
        original_duration = len(audio)

        if original_duration > max_duration:
            trimmed_audio = audio[:max_duration]
            if output_path is None:
                output_path = file_path  # Overwrite original file
            trimmed_audio.export(output_path, format=get_format(file_path))
            print(f"Trimmed '{file_path}' from {ms_to_time(original_duration)} to {ms_to_time(max_duration)}.")
        else:
            print(f"Skipped '{file_path}' (duration {ms_to_time(original_duration)} is under the limit).")

    except Exception as e:
        print(f"Error processing '{file_path}': {e}")

def get_format(file_path):
    """
    Extracts the file format from the file extension.

    :param file_path: Path to the audio file.
    :return: File format string compatible with pydub/export.
    """
    return os.path.splitext(file_path)[1][1:].lower()

def ms_to_time(milliseconds):
    """
    Converts milliseconds to a time string in MM:SS format.

    :param milliseconds: Time in milliseconds.
    :return: Formatted time string.
    """
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02}"

def process_directory(directory, overwrite=True):
    """
    Processes all supported audio files in the given directory.

    :param directory: Path to the directory containing audio files.
    :param overwrite: If True, overwrites the original files. Otherwise, saves trimmed files with a suffix.
    """
    if not os.path.isdir(directory):
        print(f"The directory '{directory}' does not exist or is not a directory.")
        return

    for filename in os.listdir(directory):
        if filename.lower().endswith(SUPPORTED_FORMATS):
            file_path = os.path.join(directory, filename)
            if overwrite:
                trim_audio(file_path)
            else:
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}_trimmed{ext}"
                output_path = os.path.join(directory, new_filename)
                trim_audio(file_path, output_path=output_path)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Trim all audio files in a directory to 2 minutes and 32 seconds.")
    parser.add_argument("directory", help="Path to the target directory containing audio files.")
    parser.add_argument(
        "--output", 
        choices=["overwrite", "copy"], 
        default="overwrite",
        help="Choose whether to overwrite the original files or save trimmed copies. Default is overwrite."
    )

    args = parser.parse_args()

    if args.output == "overwrite":
        process_directory(args.directory, overwrite=True)
    else:
        process_directory(args.directory, overwrite=False)