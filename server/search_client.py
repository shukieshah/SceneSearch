from elasticsearch import Elasticsearch
from elasticsearch import helpers


class SearchClient():
    def __init__(self, search_field):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        self.search_field = search_field

    def __create_index(self, index_name):
        options = '''
        {
          "settings": {
            "analysis": {
              "analyzer": {
                "my_analyzer": {
                  "tokenizer": "standard",
                  "filter": [ "lowercase", "stop" ]
                }
              }
            }
          },
          "mappings": {
            "properties": {
              "%s": {
                "type": "search_as_you_type"
              },
              "%s_vector": {
                "type": "dense_vector",
                "dims": 512
              }
            }
          }
        }''' % (self.search_field, self.search_field)
        self.es.indices.create(index_name, body=options)

    def __build_search_as_you_type_query(self, search_phrase):
        query = {
            "multi_match": {
                "query": search_phrase,
                "type": "bool_prefix",
                "fields": [
                    self.search_field,
                    "%s._2gram" % self.search_field,
                    "%s._3gram" % self.search_field
                ],
            "fuzziness": "AUTO"
            }
        }
        return query

    def __build_search_similar_query(self, query_vector):
        query = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, doc['%s_vector']) + 1.0" % self.search_field,
                    "params": {"query_vector": query_vector}
                }
            }
        }
        return query

    def __refresh_index(self, index_name):
        self.es.indices.refresh(index=index_name)

    def index_documents(self, documents, index_name):
        if not self.es.indices.exists(index_name):
            self.__create_index(index_name)
        actions = [{ "_index": index_name, "_id": i, "_source": documents[i] } for i in range(len(documents))]
        helpers.bulk(self.es, actions)
        self.__refresh_index(index_name)

    def search_as_you_type(self, search_phrase, index_name, topk=3):
        res = self.es.search(
            index = index_name,
            size = topk,
            body = {
                "query": self.__build_search_as_you_type_query(search_phrase),
                "_source": {"exclude": ["%s_vector" % self.search_field]}
            }
        )
        return [(hit["_score"], hit["_source"]) for hit in res['hits']['hits']]

    def search_similar(self, query_vector, index_name, topk=3):
        res = self.es.search(
            index = index_name,
            size = topk,
            body = {
                "query": self.__build_search_similar_query(query_vector),
                "_source": {"exclude": ["%s_vector" % self.search_field]}
            }
        )
        return [(hit["_score"], hit["_source"]) for hit in res['hits']['hits']]
