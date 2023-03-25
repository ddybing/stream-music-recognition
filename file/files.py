import asyncio
import math
import os
import re
import time

from shazamio import Shazam
from pydub import AudioSegment

shazam = Shazam()

path_to_dir = "../file_samples"
music_segment_duration = 30000  # milliseconds
check_delay = 1  # seconds
output_file = "./songs.txt"
skip_chunk = 2  # 1 - every, 2 - odd ...


# for sort chunks
def try_int(s):
    try:
        return int(s)
    except:
        return s


def alphanum_key(s):
    return [try_int(c) for c in re.split('([0-9]+)', s)]


def split_audio_file(input_file_path, output_folder_path):
    audio = AudioSegment.from_file(input_file_path, format="mp3")
    chunk_length_ms = music_segment_duration

    # Split the audio file into chunks of length 30 seconds
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    print(f"{math.ceil(len(audio) / chunk_length_ms / skip_chunk)} fragments (length: {len(audio)})")
    print("Create...")
    for i, chunk_start in enumerate(range(0, len(audio), chunk_length_ms)):
        if i % skip_chunk == 0:
            chunk = audio[chunk_start:chunk_start + chunk_length_ms]

            # Save the chunk to a file
            output_file_path = os.path.join(output_folder_path, f"chunk_{i}.mp3")
            chunk.export(output_file_path, format="mp3")


async def recognize(path):
    out = await shazam.recognize_song(path)
    if "track" in out:
        with open(output_file, 'r+') as write_file:
            current_song = out["track"]["subtitle"] + " - " + out["track"]["title"]
            if any(current_song == x.rstrip('\r\n') for x in write_file):
                print(f"Duplicate ({current_song})")
            else:
                print(f"New song: {current_song}")
                write_file.write(current_song + '\n')
    else:
        print("Undefined segment :(")


async def main():
    files = [f for f in os.listdir(path_to_dir) if os.path.isfile(os.path.join(path_to_dir, f))]
    for file in files:
        split_folder = file.split(".")[0]
        split_audio_file(os.path.join(path_to_dir, file), os.path.join(path_to_dir, split_folder))
        path_to_split_folder = os.path.join(path_to_dir, split_folder)
        split_files = [f for f in os.listdir(path_to_split_folder) if
                       os.path.isfile(os.path.join(path_to_split_folder, f))]
        split_files = sorted(split_files, key=alphanum_key)
        print("Recognize...")
        for split_file in split_files:
            time.sleep(check_delay)
            await recognize(os.path.join(path_to_split_folder, split_file))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
