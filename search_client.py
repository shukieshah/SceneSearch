from elasticsearch import Elasticsearch
from elasticsearch import helpers


class SearchClient():
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def bulk_index(self, documents, index_name):
        actions = [{ "_index": index_name, "_id": i, "_source": documents[i] } for i in range(len(documents))]
        helpers.bulk(self.es, actions)
        self.refresh_index(index_name)

    def index_document(self, document, index_name):
        res = self.es.index(index=index_name, body=document)
        self.refresh_index(index_name)
        return res['result']

    def refresh_index(self, index_name):
        self.es.indices.refresh(index=index_name)

    def search(self, search_phrase, index_name, search_field, topk=10):
        res = self.es.search(index=index_name, size=topk, body={"query": {"match": { search_field: search_phrase }}})
        return [(hit["_score"], hit["_source"]) for hit in res['hits']['hits']]
