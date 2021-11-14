from elasticsearch import Elasticsearch
from dotenv import load_dotenv
load_dotenv()
import os

class ElasticsearchConnection(object):
    '''
        A class to inialize a connection to an elasticsearch deployment
    '''

    def __init__(self):
        #read deployment credentials
        cloud_id = os.environ.get("CLOUD_ID")
        http_auth_user = os.environ.get("HTTP_AUTH_USER")
        http_auth_password = os.environ.get("HTTP_AUTH_PASSWORD")

        #attempt to initalize connection
        try:
            self.es = Elasticsearch(
                cloud_id=cloud_id,
                http_auth=(http_auth_user, http_auth_password),
                )
        except Exception as err:
            print('Could not connect to Elasticsearch deployment: ' + str(err))