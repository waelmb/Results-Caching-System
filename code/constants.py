BACKEND_URL = 'http://127.0.0.1:8000/'
SEARCH_REQUEST_BODY =  {
         "searchTerm": "covid",
         "searchFilter":{
                "sources": [{ "label": "UpToDate","value": "UpToDate", "group":"EBM","disabled": False },
                            { "label": "DynaMed","value": "DynaMed", "group":"EBM",  "disabled": False},
                            { "label": "PubMed","value": "PubMed", "group":"Journals",  "disabled": False },
                            { "label": "MayoClinic","value": "MayoClinic","group":"Web resources",  "disabled": False},
                            { "label": "GoogleDrive","value": "GoogleDrive", "group":"Personal",  "disabled": False},
                            { "label": "Box","value": "Box", "group":"Personal",  "disabled": False}],
                "filter_highest": [{ "label": "UpToDate","value": "UpToDate", "group":"EBM","disabled": False },
                                    { "label": "PubMed","value": "PubMed", "group":"Journals",  "disabled": False }],
                "filter_high": [],
                "filter_normal": [{ "label": "DynaMed","value": "DynaMed", "group":"EBM",  "disabled": False},
                                { "label": "MayoClinic","value": "MayoClinic","group":"Web resources",  "disabled": False},
                                { "label": "GoogleDrive","value": "GoogleDrive", "group":"Personal",  "disabled": False}
                                ],
                "filter_low": [],
                "filter_lowest":[{ "label": "Box","value": "Box", "group":"Personal",  "disabled": False }]
                },
         "id":0
        }
ADD_REQUEST_BODY = {
       "results": [{
                "title": "<b><b>covid</b></b>-<b><b>19</b></b>: Diagnosis",
                "url": "https://www.uptodate.com/contents/covid-19-diagnosis?search=covid+19&source=search_result&selectedTitle=7%7E150&usage_type=default&display_rank=7",
                "source": "uptodate",
                "date": "2021-11-27T02:37:02.280213",
                "author": "",
                "abstract": "",
                "score": 1.2
            }]
       }
ES_GET_ALL_QUERY = {"query": {"match_all": {}}}