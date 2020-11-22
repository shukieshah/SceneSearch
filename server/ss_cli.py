import os
import sys
from caption import caption_video
from search_client import SearchClient
from semantic_similarity import embed_text
import pickle
import shutil

FFMPEG_BIN = "ffmpeg"
FRAME_WIDTH = "256"
FRAME_LENGTH = "256"
FRAME_OFFSET = 1
FPS = "1"

if __name__ == '__main__':

    # Example call: python ss_cli.py Video.mp4 1
    video = sys.argv[1]
    video_name = video[:-4]

    # granularity defines how frequently captions should be generated for the video
    # It essentially controls how distinguishable adjacent caption/scene pairings are from one another (to prevent duplicates)
    # Example: granularity of 3 would generate captions for every third frame/second of the video
    granularity = int(sys.argv[2])
    pickle_filename = "./saved_caption_timestamps/%s_caption_timestamps_granularity_%s.pickle" % (video_name, granularity)

    # Load captions & timestamps if they already exist
    if os.path.isfile(pickle_filename):
        with open(pickle_filename, 'rb') as pickle_file:
            caption_timestamps = pickle.load(pickle_file)
    else:
        folder = "./video_frames_%s/" % video_name
        if not os.path.exists(folder):
            os.makedirs(folder)

            # Run the ffmpeg video parser to extract individual frame images
            os.system(FFMPEG_BIN + " -i " + video + " -r " + FPS + " -loglevel quiet -vf scale=" + \
                        FRAME_WIDTH + ":" + FRAME_LENGTH + " " + folder + "image-%08d.png")

        caption_timestamps = caption_video(folder, granularity=granularity, frame_offset=FRAME_OFFSET)

        # Pickle (serialize) the caption timestamps and save them to disk for later use
        with open(pickle_filename, 'wb') as pickle_file:
            pickle.dump(caption_timestamps, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)

        shutil.rmtree(folder)

    # Compute and store the sentence embedding for each caption
    captions = [doc["caption"] for doc in caption_timestamps]
    caption_vectors = embed_text(captions)

    for i, doc in enumerate(caption_timestamps):
        doc["caption_vector"] = caption_vectors[i]

    searchClient = SearchClient(search_field="caption")
    searchClient.index_documents(caption_timestamps, video_name)

    while True:
        search_phrase = input("\nEnter a search phrase >> ")
        top_matches = searchClient.search_as_you_type(search_phrase, video_name)
        print("\nTop %d Search As You Type Matches:" % len(top_matches))

        for result in top_matches:
            print("-"*60)
            print("SCORE: %s" % result["score"])
            print("CAPTION: %s" % match["document"]["caption"])
            print("TIMESTAMP: %s" % match["document"]["timestamp"])

        top_matches = searchClient.search_similar(embed_text([search_phrase])[0], video_name)
        print("\nTop %d Similar Matches:" % len(top_matches))

        for result in top_matches:
            print("-"*60)
            print("SCORE: %s" % result["score"])
            print("CAPTION: %s" % match["document"]["caption"])
            print("TIMESTAMP: %s" % match["document"]["timestamp"])
