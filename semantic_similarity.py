import tensorflow_hub as hub
import tensorflow as tf
from scipy.spatial import distance
import numpy as np
import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'
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
    min_index = np.argmin(distances)
    min_distance = distances[min_index]
    max_similarity = 1 - min_distance

    return (captions[min_index], max_similarity)
