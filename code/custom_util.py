import requests
import json
import threading
from math import log

def request_task(url, body, headers):
    requests.post(url, data=json.dumps(body), headers=headers)

def fire_and_forget(url, body, headers):
    threading.Thread(target=request_task, args=(url, body, headers)).start()

def score_raw(data,source_weight=1):
    """
    generate the scoring for result with scoring from source

    :param data:
       list data dictionary properties with scores from sources
    :type data:
       `list[data[unicode]`
    :param source_weight:
        current source 'value'
    :type source_weight:
        `float`
    :return:
       list data dictionary properties with scores normalize
    :rtype:
       `list[data[unicode]`
    """
    if len(data) == 0:
        return data
    data.sort(key=lambda hit: hit['score'], reverse=True)
    max_score = data[0]["score"]
    if max_score == 0.0:
        return data

    min_score = data[len(data) - 1]["score"]

    if max_score - min_score == 0.0:
        min_score = 0
    for file in data:
        title_weight = 1.0
        normalized_score = log(1 + ((file["score"] - min_score) / (max_score - min_score)), 2)
        if normalized_score == 0:
            normalized_score = 0.05
        file["score"] = source_weight * normalized_score * title_weight

    return data

def get_results(response):
    """
    get each data in response and index it
    :param response:
         list of dictionary of data that matched the query
    :type  response:
        `list[dict[unicode,any]]`
    :return:
        list of dictionary where each dictionary contains each file properties value
    :rtype:
        `list[dict[unicode,any]]`
    """
    results = []
    # loop through elastic search results
    for file in response:
        abstract = " "

        # get the abstract
        if file.get("highlight") is not None:
            if file["highlight"].get("title") is not None:
                abstract += (" ".join(file["highlight"]['title']))
            if file["highlight"].get("abstract") is not None:
                abstract += (" ".join(file["highlight"]['abstract']))

        # clean the abstract
        abstract = abstract.replace("<em>", "<b>").replace("</em>", "</b>").strip()

        # reindex the file
        author = 'author'
        if file["_source"].get('author') is not None:
            author = file["_source"]['author']
        title = "None"
        if file["_source"]['title'] is not None:
            title = file["_source"]['title']

        source_name = ""
        if file["_source"].get('type') is not None:
            source_name = file["_source"]['type']

        properties = {"title":title, "url": file["_id"],
                      "source": source_name, "date": file["_source"]['date'], "author": author,
                      "abstract": abstract, "score":file["_score"] }

        results.append(properties)
        if len(results) >= 10:
            break

    # normalize the score
    results = score_raw(results,0.5)

    return results
