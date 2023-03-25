import asyncio
import time

from shazamio import Shazam
import sys

path_to_dir = "../stream_samples/"
segment_file = "segment_list.txt"
check_delay = 1  # (seconds) limit requests for Shazam
output_file = "./songs.txt"

sys.path.append('/snap/bin/ffmpeg')
shazam = Shazam()


async def recognize(path, write_file):
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
    with open(path_to_dir + segment_file, "r") as file:
        for index, line in enumerate(file):
            if index % 2 == 0:  # check odd elements for increase speed
                time.sleep(check_delay)
                await recognize(path_to_dir + line.rstrip())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
