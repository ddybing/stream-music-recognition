Some python scripts for recognize songs via Shazam on audio streams and files

# Stream music recognition via Shazam
Recognize songs in real-time from a streaming audio source and writes the recognized songs to a file using the Shazam API. 
It can be used to identify songs played on live radio, music streaming services, or any other audio stream.

If you want to work with an audio stream, need to get its small fragments (30-60s). I recommend use ffmpeg and this command:

`ffmpeg -i https://silverrain.hostingradio.ru/silver128.mp3 -codec copy -f segment -segment_format_options "id3v2_version=0:write_id3v1=0:write_xing=0" -segment_list segment_list.txt -segment_list_type flat -segment_time 30 -strftime 1 %Y-%m-%d_%H-%M-%S.mp3`

- https://silverrain.hostingradio.ru/silver128.mp3 - your audio stream
- segment_list - write all file names on segment_list.txt in command execution path
- segment_time - fragment duration (s)


### Segments recognition (after_stream.py)
   
Code reads an audio fragments from a directory in file segment_list.txt and performs song recognition using the Shazam API. The recognized songs are then written to a file. If the song is recognized, the song information is added to an output file. 

The script requires the following inputs:

- path_to_dir: the path to the directory where the segments are stored
- segment_file: this is the name of the file containing a list of the music file segments to be recognized. Each line of the file should contain the filename of a segment to be recognized, relative to path_to_dir.
- check_delay: the delay in seconds between each segment recognition request to the Shazam API (default is 1 second)
- output_file: the file path where the recognized songs will be written to (default is "./songs.txt")
   
### Real-time segments recognition (realtime.py)
   
The code uses the watchdog library to monitor a directory and waits for new audio files to be created. 
   
Once a new audio file is created, the code waits when file is complete to record, and then sends the audio segment to the Shazam API to recognize the song. 

The script requires the following inputs:

- path_to_dir: the path to the directory where the segments are stored
- music_extension: the file extension of the music files which are caught on creating (default is "mp3")
- music_segment_duration: the duration of each music segment in milliseconds (default is 30 seconds) and don't forget change music_segment_duration like your segment_time on ffmpeg
- output_file: the file path where the recognized songs will be written to (default is "./songs.txt")


# File music recognition via Shazam (files.py)

Code designed to split music files into 30-second chunks and then search each part using the Shazam API to recognize the song in each chunk. By splitting the music file into smaller segments the script can identify the individual songs within the larger file like music program recording and various music mixes. 

The script requires the following inputs:

- path_to_dir: the path to the directory where the music files are stored
- music_segment_duration: the duration of each music segment in milliseconds (default is 30 seconds)
- check_delay: the delay in seconds between each segment recognition request to the Shazam API (default is 1 second)
- output_file: the file path where the recognized songs will be written to (default is "./songs.txt")
- skip_chunk: the number of chunks to skip before processing the next chunk (default is 2, which skips every other chunk)



