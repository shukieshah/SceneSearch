from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json
import tensorflow as tf
from caption import caption_video
from search_client import SearchClient
from semantic_similarity import embed_text
from video_utils import download_yt_video, extract_video_frames

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/process_video')
@cross_origin()
def process_video():
    video_id = request.args.get('video_id', '')
    granularity = int(request.args.get('granularity', ''))
    video_frames_path = "../client/scene-search-react-app/public/images/video_frames_%s/" % video_id

    try:
        download_yt_video(video_id)
    except Exception:
        return jsonify({"success": False, "error_message": "invalid youtube video id"})

    extract_video_frames(video_frames_path, video_id)
    caption_timestamps = caption_video(video_frames_path, granularity=granularity, frame_offset=1)

    # Compute and store the sentence embedding for each caption
    captions = [doc["caption"] for doc in caption_timestamps]
    caption_vectors = embed_text(captions)

    for i, doc in enumerate(caption_timestamps):
        doc["caption_vector"] = caption_vectors[i]

    searchClient.index_documents(caption_timestamps, video_id.lower())
    return jsonify({"success": True})

@app.route('/search_as_you_type')
@cross_origin()
def search_as_you_type():
    video_id = request.args.get('video_id', '')
    search_phrase = request.args.get('search_phrase', '')

    try:
        results = searchClient.search_as_you_type(search_phrase, video_id.lower())
        return jsonify({"results": results})
    except Exception:
        return jsonify({"results": [], "error_message": "invalid video id"})


@app.route('/search_similar')
@cross_origin()
def search_similar():
    video_id = request.args.get('video_id', '')
    search_phrase = request.args.get('search_phrase', '')

    try:
        results = searchClient.search_similar(embed_text([search_phrase])[0], video_id.lower())
        return jsonify({"results": results})
    except Exception:
        return jsonify({"results": [], "error_message": "invalid video id"})

if __name__ == '__main__':
    searchClient = SearchClient(search_field="caption")
    app.run()
