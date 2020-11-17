import tensorflow_hub as hub
import tensorflow as tf
from scipy.spatial import distance
import numpy as np
import os

os.environ["KMP_DUPLICATE_LIB_OK"]= "True"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TFHUB_CACHE_DIR"] = "/Users/shukan/Workspace/tf_cache"
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

session = tf.compat.v1.Session()
session.run([tf.compat.v1.global_variables_initializer(), tf.compat.v1.tables_initializer()])

def embed_text(text):
    embeddings = session.run(embed(text))
    return [embedding.tolist() for embedding in embeddings]

# def topk_similar(target, captions, embedding_matrix, topk=3):
#     target_embedding = session.run(embed(target))
#     distances = distance.cdist(target_embedding, embedding_matrix, "cosine")[0]
#     topk_indices = np.argsort(distances)[:topk]
#     topk_results = [(captions[idx], 1 - distances[idx]) for idx in topk_indices]
#     return topk_results
