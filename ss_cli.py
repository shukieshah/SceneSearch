import os
import sys
from caption import caption_video
from semantic_similarity import encode_captions, topk_similar
import numpy as np

if __name__ == '__main__':
    FFMPEG_BIN = "ffmpeg"
    FRAME_WIDTH = "256"
    FRAME_LENGTH = "256"
    FPS = 1

    #Example call: python ss_cli.py Video.mp4 1
    video = sys.argv[1]
    granularity = int(sys.argv[2])

    #The folder that the frame images will end up in
    folder = "./video_frames/"
    if not os.path.exists(folder):
        os.makedirs(folder)

    #Run the parser to generate the frame images
    if not len(os.listdir(folder)):
        os.system(FFMPEG_BIN + " -i " + video + " -r " + FPS + " -vf scale=" + \
                    FRAME_WIDTH + ":" + FRAME_LENGTH + " " + folder + "image-%08d.png")

    caption_timestamps = caption_video(folder, granularity)
    captions = [caption for caption in caption_timestamps]
    caption_embeddings = encode_captions(captions)

    while True:
        search_phrase = input("\nEnter a search phrase >> ")
        most_similar_caption, similarity_score = topk_similar([search_phrase], captions, caption_embeddings)
        print("\nCLOSEST CAPTION: %s" % most_similar_caption)
        print("SIMILARITY SCORE: %s" % most_similar_caption)
        print("TIMESTAMP: %s" % caption_timestamps[most_similar_caption])
