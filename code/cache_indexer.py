from copy import Error
from elasticsearch import helpers
from elasticsearch_connection import ElasticsearchConnection
import datetime



"""
Adapted from sample_es_indexer.py by Bhavya
"""

class CacheIndexer(object):
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
        self.index_name = "search_cache"
        self.doc_num_threshold = 10000
        self.files = files
        self.es = ElasticsearchConnection().es

        # check index name exist, if not create one
        if not self.index_exist():
            self.es.indices.create(
                index=self.index_name,
                body={
                    "mappings": {
                        "properties": {
                            "title": {"type": "text", "fielddata": True},
                            "url": {"type": "text", "fielddata": True},
                            "date": {"type": "date", "format": "date_optional_time"},
                            "author": {"type": "text", "fielddata": True},
                            "abstract": {"type": "text", "analyzer": "english", "fielddata": True},
                        }
                    }
                },
            )
        #Shard Request Cache is enabled by default


    @property
    def es_client(self):
        """
        :return:
            elastic client
        :rtype:
            `object`
        """
        return self.es
    """ @property
    def index_name(self): """
    """
    :return:
        elastic client
    :rtype:
        `object`
    """
    """ return self.index_name """

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
        # temp_files = self.files
        # for file in self.files:
        #     # find data that has the exact same id
        #     query = {"query": {"match_phrase": {"_id": file["url"]}}}

        #     # if exist, check if the existing file is older. If not add to  to_be_removed_file
        #     for i, existing_file in enumerate(
        #             helpers.scan(client=self.es, query=query, index=self.index_name, size=10000,
        #                          preserve_order=True, request_timeout=10)):
        #         # remove from list of file id
        #         temp_files.remove(existing_file)
        # self.files = temp_files

        for file in self.files:
            yield {
                "_index": self.index_name,
                "_id": file["url"],
                "_source": file["source"],
            }
    # Does body need to match 1-search?
    #TODO: Check for duplicates, use url as id!
    # The latest document will simply override the previous one having the same ID and the version count will be bumped by 1.
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
                            "title": {"type": "text", "fielddata": True},
                            "url": {"type": "text", "fielddata": True},
                            "date": {"type": "date", "format": "date_optional_time"},
                            "author": {"type": "text", "fielddata": True},
                            "abstract": {"type": "text", "analyzer": "english", "fielddata": True},
                        }
                    }
                },
            )

        try:
            #TODO:Take apart helpers.bulk
            helpers.bulk(self.es, self.gendata())  # indexing and uploading all files
            self.refresh_index()
            print("Documents in " + self.index_name + ": ", self.es.cat.count(self.index_name, params={"format": "json"}))
        except Exception as err:
            print('bulk herlper error', str(err))
    '''Sample query should be:
    {
    "query": { 
        "bool": { 
        "must": [
            { "match": { "title":   "Search"        }},
            { "match": { "content": "Elasticsearch" }}
        ],
        "filter": [ 
            { "term":  { "status": "published" }},
            { "range": { "publish_date": { "gte": "2015-01-01" }}}
        ]
        }
    }
    }
    '''
    def search_index(self, query= {"query": {"match_all": {}}}):
        """
            search an index
        """
        start_time = datetime.datetime.today()
        if self.index_exist():
            try:
                
                max_results = 50
                response = self.es.search(body=query, index=self.index_name, scroll='2m', size=max_results)
                results = response["hits"]['hits']
                # results = helpers.scan(self.es,
                #     index=self.index_name,
                #     preserve_order=True,
                #     query=query,)
                end_time = datetime.datetime.today()
                time_delta = (end_time - start_time)
                total_seconds = time_delta.total_seconds()
                return results, str(round(total_seconds, 2))
            except Exception as err:
                print('Helpers.scan could not execute', str(err))
                end_time = datetime.datetime.today()
                time_delta = (end_time - start_time)
                total_seconds = time_delta.total_seconds()
                return [], str(round(total_seconds, 2))
        else:
            print('search_index: Index does not exist')
            end_time = datetime.datetime.today()
            time_delta = (end_time - start_time)
            total_seconds = time_delta.total_seconds()
            return [], str(round(total_seconds, 2))
           
    def delete_index(self):
        """
        delete the index
        """
        if self.index_exist():
            self.es.indices.delete(index=self.index_name, ignore=[400, 404])  # deleting existing index
    
    def refresh_index(self):
        """
        refresh the index
        """
        if self.index_exist():
            self.es.indices.refresh(index=self.index_name) # refresh existing index
            
    def index_clean_up(self):
        query = {"sort": { "date": "asc"},"query": {"match_all": {}}}
        for i,file in enumerate(helpers.scan(self.es,index=self.index_name,preserve_order=True,query=query,)):
            if i > self.doc_num_threshold:
                break
            self.es.delete(index=self.index_name, doc_type="_doc", id=file["_id"])