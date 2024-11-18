# The Oddly Specific Audio Trim Python Script

This script trims all audio files in a directory to 2 minutes and 32 seconds.

# How to Use the Script

### 1 Save the Script: Save the python script to your machine.
### 2 Run the Script:

Open your terminal or command prompt and navigate to the directory where trim_audio.py is saved.

`python trim_audio.py /path/to/your/audio/directory`

By default, this will overwrite the original audio files if they exceed 2 minutes and 32 seconds.

### 3 Saving Trimmed Copies Instead of Overwriting:

If you prefer to keep the original files and save the trimmed versions separately, use the --output copy option:

`python trim_audio.py /path/to/your/audio/directory --output copy`

This will save the trimmed files with a _trimmed suffix. For example, song.mp3 will become song_trimmed.mp3.
