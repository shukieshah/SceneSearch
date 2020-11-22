import tensorflow_hub as hub
import tensorflow as tf
import os

os.environ["KMP_DUPLICATE_LIB_OK"]= "True"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TFHUB_CACHE_DIR"] = "/Users/shukan/Workspace/tf_cache"

g = tf.Graph()
with g.as_default():
  # We will be feeding 1D tensors of text into the graph.
  text_input = tf.compat.v1.placeholder(dtype=tf.string, shape=[None])
  embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
  embedded_text = embed(text_input)
  init_op = tf.group([tf.compat.v1.global_variables_initializer(), tf.compat.v1.tables_initializer()])
g.finalize()

session = tf.compat.v1.Session(graph=g)
session.run(init_op)

def embed_text(text):
    embeddings = session.run(embedded_text, feed_dict={text_input: text})
    return [embedding.tolist() for embedding in embeddings]
