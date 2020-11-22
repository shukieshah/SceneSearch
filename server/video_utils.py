from pytube import YouTube
import os
import sys

FFMPEG_BIN = "ffmpeg"
FRAME_WIDTH = "256"
FRAME_LENGTH = "256"
FPS = "1"

def download_yt_video(video_id):
    yt = YouTube("https://www.youtube.com/watch?v=%s" % video_id)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
    files = os.listdir(".")
    for f in files:
        if f.endswith('.mp4'):
            os.rename(f, "%s.mp4" % video_id)
            return


def extract_video_frames(folder, video_name):
    if not os.path.exists(folder):
        os.makedirs(folder)

        # Run the ffmpeg video parser to extract individual frame images
        os.system(FFMPEG_BIN + " -i " + video_name + ".mp4" + " -r " + FPS + " -loglevel quiet -vf scale=" + \
                    FRAME_WIDTH + ":" + FRAME_LENGTH + " " + folder + "image-%08d.png")
        os.remove("%s.mp4" % video_name)
