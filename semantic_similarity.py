import tensorflow_hub as hub
import tensorflow as tf
from scipy.spatial import distance
import numpy as np
import os

os.environ['KMP_DUPLICATE_LIB_OK']= 'True'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

def encode_captions(captions):
    with tf.compat.v1.Session() as session:
        session.run([tf.compat.v1.global_variables_initializer(), tf.compat.v1.tables_initializer()])
        caption_embeddings = session.run(embed(captions))
    return caption_embeddings

def topk_similar(target, captions, embedding_matrix, topk=3):
    with tf.compat.v1.Session() as session:
        session.run([tf.compat.v1.global_variables_initializer(), tf.compat.v1.tables_initializer()])
        target_embedding = session.run(embed(target))

    distances = distance.cdist(target_embedding, embedding_matrix, "cosine")[0]
    topk_indices = np.argsort(distances)[:topk]
    topk_results = [(captions[idx], 1 - distances[idx]) for idx in topk_indices]
    return topk_results
