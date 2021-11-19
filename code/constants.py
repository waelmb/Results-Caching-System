BACKEND_URL = 'http://127.0.0.1:8000/'
SEARCH_REQUEST_BODY =  {
         "searchTerm": "",
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

ES_GET_ALL_QUERY = {"query": {"match_all": {}}}