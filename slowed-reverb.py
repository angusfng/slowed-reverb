import sys
import moviepy.editor as mp
import math
import os
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from pysndfx import AudioEffectsChain
from PIL import Image

# Usage: <audio> <gif>
def main():
    # Moved flag for webp
    moved = 0
    # Get the file paths from arguments
    audio = sys.argv[1]
    gif = sys.argv[2]

    # Handling webp to gif
    if gif.endswith(".webp"):
        print("Converting webp to gif")
        im = Image.open(gif)
        im.save("a.gif", 'gif', save_all=True)
        os.rename(gif, "oldgif/{}".format(gif))
        moved = 1
        gif = "a.gif"

    # Construct title for youtube video
    mp3 = MP3File(audio)
    tags = mp3.get_tags()
    tags = tags["ID3TagV1"]
    title = tags["artist"] + " - " + tags["song"] + " (slowed + reverb)"

    # Path to put final mp4
    outputPath = "output/a.mp4"

    # Printing audio file
    audioNoSpace = audio.replace(" ", "")
    os.rename(audio, audioNoSpace)
    audio = audioNoSpace
    print("Converting " + audio)

    # Parameters for the slowing and reverb
    fx = (
        AudioEffectsChain()
        .speed(0.85)
        .reverb()
    )

    # Temporary path for the slowed reverb audio mp3
    audioPath = "output/temp.mp3"

    # Perform the slow and reverb
    print("Performing slow reverb")
    fx(audio, audioPath)

    # Get the slowed reverb audio mp3
    audioClip = mp.AudioFileClip(audioPath)

    # Get the gif
    videoClip = mp.VideoFileClip(gif)

    # Calculate number of time it needs to loop and put into video
    numLoops = math.ceil(audioClip.duration / videoClip.duration)
    videoClip2 = videoClip.loop(n=numLoops)

    # Put in the slowed reverb audio
    videoClip3 = videoClip2.set_audio(audioClip)

    print("Creating mp4")
    # Write out to mp4 in output file
    videoClip3.write_videofile(outputPath, verbose=False, logger=None)
    print("Video created")
    print(title)

    # Move to old audio and gif file
    #os.remove(audio)
    if moved == 0:
        os.rename(gif, "oldgif/{}".format(gif))

if __name__ == "__main__":
    main()