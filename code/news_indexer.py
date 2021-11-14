from elasticsearch import helpers
from elasticsearch_connection import ElasticsearchConnection

"""
Adapted from sample_es_indexer.py by Bhavya
"""

class NewsIndexer(object):
    """
        For indexing and uploading to elastic search.
    """
    def __init__(
            self,
            files=None,
    ):
        """
        :param index_name:
            index name that will show in kibana
        :type index_name:
            `unicode`
        :param files:
            list of dictionary where each dictionary contains each file properties value
        :type files:
            ` list[dict[dict[unicode], dict[unicode]]]`
        """
        self.index_name = "medical_news"
        self.files = files
        self.es = ElasticsearchConnection().es


    @property
    def es_client(self):
        """
        :return:
            elastic client
        :rtype:
            `object`
        """
        return self.es

    def index_exist(self):
        """
        :return:
            true if index exist
        :rtype:
            `bool`
        """
        return self.es.indices.exists(index=self.index_name)

    def gendata(self):
        """
        for generating data into elasticsearch
        specify each field with the corresponding data
        """
        for file in self.files:
            yield {
                "_index": self.index_name,
                "_id": file["_id"],
                "_source": file["source"],
            }

    def upload(self):
        """
        For uploading and authenticating to elasticsearch cloud
        create/update index file on the elasticsearch cloud
        replace the properties mapping according to the file data types
        """

        # check index name exist, if so then delete current one
        if not self.index_exist():
            self.es.indices.create(
                index=self.index_name,
                body={
                    "mappings": {
                        "properties": {
                            "article": {"type": "text", "analyzer": "english", "fielddata": True},
                        }
                    }
                },
            )

        try:
            helpers.bulk(self.es, self.gendata())  # indexing and uploading all files
            self.refresh_index()
            print("Documents in " + self.index_name + ": ", self.es.cat.count(self.index_name, params={"format": "json"}))
        except Exception as err:
            print('bulk herlper error', str(err))


    def delete_index(self):
        """
        delete the index
        """
        self.es.indices.delete(index=self.index_name, ignore=[400, 404])  # deleting existing index
    
    def refresh_index(self):
        """
        refresh the index
        """
        if self.index_exist():
            self.es.indices.refresh(index=self.index_name) # refresh existing index