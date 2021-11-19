from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import uvicorn
from news_indexer import NewsIndexer
from crawler import JavaScript_scrape
from datetime import datetime
from constants import BACKEND_URL, SEARCH_REQUEST_BODY
import copy
from elasticsearch_connection import ElasticsearchConnection
from custom_util import fire_and_forget


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World! This is a results caching microservice for 1-Search.uic.edu"}

@app.on_event("startup") # comment during dev, uncomment in production
@repeat_every(seconds=60 * 60)  # 1 hour
async def update_trendy_topics() -> None:
    '''
        A function that executes periodically to update the medical_news index with the latest trendy topics
    '''
    # calculate initial time
    print('Initializing topics update..')
    initial_time = datetime.today()

    # delete previously stored trendy topics
    '''NewsIndexer().delete_index()

    # crawl trendy topics and store to elasticsearch
    JavaScript_scrape().scrape_webMD(output='elasticsearch')
    JavaScript_scrape().scrape_medscape(output='elasticsearch')
    JavaScript_scrape().scrape_aapNews(output='elasticsearch')
    JavaScript_scrape().scrape_medicalNewsToday(output='elasticsearch')

    # get results from elasticsearch
    # formatted as: [{'_index': 'medical_news', '_type': '_doc', '_id': 'url', '_score': 1.0, '_source': {'article': 'text'}}
    try:
        results = list(NewsIndexer().search_index())
        print('Results from elasticsearch', len(results))
    except Exception as err:
        print('Could not get results from elasticsearch', str(err))'''

    # fetch results and pass to topic modeling/keyword extraction algorithms
    keywords = ['covid']

    # call search endpoint and update cache
    for keyword in keywords:
        body = copy.deepcopy(SEARCH_REQUEST_BODY)
        body['searchTerm'] = keyword
        headers= {"content-type":"application/json"}
        try:
            fire_and_forget(url=BACKEND_URL+'search/', body=body, headers=headers)
        except Exception as err:
            print('Could not call search endpoint for keyword: ' + keyword + '. The following error occured: ' + str(err))

    # output total time
    delta_time = str(round((datetime.today() - initial_time).total_seconds(), 2))
    print('Topics update completed with total time', delta_time)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8001)