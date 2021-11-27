from fastapi import FastAPI, Request
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json     
from news_indexer import NewsIndexer
from crawler import JavaScript_scrape
from datetime import datetime
from constants import BACKEND_URL, SEARCH_REQUEST_BODY
import copy
from elasticsearch_connection import ElasticsearchConnection
from custom_util import fire_and_forget


app = FastAPI()

# CORS origins
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/test")
async def test(request: Request):
    try:
        requestJson = await request.json()
    except Exception as err:
        print('Could not read JSON: ' + err)
  
    response = {
        "count": 30,
        "searchTerm": requestJson['searchTerm'],
        "time": "26.97",
        "searchFilter": {
            "sources": [
                {
                    "label": "UpToDate",
                    "value": "UpToDate",
                    "group": "EBM",
                    "disabled": False
                },
                {
                    "label": "DynaMed",
                    "value": "DynaMed",
                    "group": "EBM",
                    "disabled": False
                },
                {
                    "label": "PubMed",
                    "value": "PubMed",
                    "group": "Journals",
                    "disabled": False
                },
                {
                    "label": "MayoClinic",
                    "value": "MayoClinic",
                    "group": "Web resources",
                    "disabled": False
                },
                {
                    "label": "GoogleDrive",
                    "value": "GoogleDrive",
                    "group": "Personal",
                    "disabled": False
                },
                {
                    "label": "Box",
                    "value": "Box",
                    "group": "Personal",
                    "disabled": False
                }
            ],
            "filter_highest": [
                {
                    "label": "UpToDate",
                    "value": "UpToDate",
                    "group": "EBM",
                    "disabled": False
                },
                {
                    "label": "PubMed",
                    "value": "PubMed",
                    "group": "Journals",
                    "disabled": False
                }
            ],
            "filter_high": [],
            "filter_normal": [
                {
                    "label": "DynaMed",
                    "value": "DynaMed",
                    "group": "EBM",
                    "disabled": False
                },
                {
                    "label": "MayoClinic",
                    "value": "MayoClinic",
                    "group": "Web resources",
                    "disabled": False
                },
                {
                    "label": "GoogleDrive",
                    "value": "GoogleDrive",
                    "group": "Personal",
                    "disabled": False
                }
            ],
            "filter_low": [],
            "filter_lowest": [
                {
                    "label": "Box",
                    "value": "Box",
                    "group": "Personal",
                    "disabled": False
                }
            ]
        },
        "results": [
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b>: Diagnosis",
                "url": "https://www.uptodate.com/contents/covid-19-diagnosis?search=covid+19&source=search_result&selectedTitle=7%7E150&usage_type=default&display_rank=7",
                "source": "uptodate",
                "date": "2021-11-27T02:37:02.280213",
                "author": "",
                "abstract": "",
                "score": 1.2
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b>: Clinical features",
                "url": "https://www.uptodate.com/contents/covid-19-clinical-features?search=covid+19&source=search_result&selectedTitle=3%7E150&usage_type=default&display_rank=3",
                "source": "uptodate",
                "date": "2021-11-27T02:37:02.279208",
                "author": "",
                "abstract": "",
                "score": 1.0929387098905343
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b>: Management in children",
                "url": "https://www.uptodate.com/contents/covid-19-management-in-children?search=covid+19&source=search_result&selectedTitle=5%7E150&usage_type=default&display_rank=5",
                "source": "uptodate",
                "date": "2021-11-27T02:37:02.279208",
                "author": "",
                "abstract": "",
                "score": 0.9878537284682086
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b>: Management in hospitalized adults",
                "url": "https://www.uptodate.com/contents/covid-19-management-in-hospitalized-adults?search=covid+19&source=search_result&selectedTitle=1%7E150&usage_type=default&display_rank=1",
                "source": "uptodate",
                "date": "2021-11-27T02:37:02.279208",
                "author": "",
                "abstract": "",
                "score": 0.8845007609964805
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b>: Epidemiology, virology, and prevention",
                "url": "https://www.uptodate.com/contents/covid-19-epidemiology-virology-and-prevention?search=covid+19&source=search_result&selectedTitle=10%7E150&usage_type=default&display_rank=10",
                "source": "uptodate",
                "date": "2021-11-27T02:37:02.280213",
                "author": "",
                "abstract": "",
                "score": 0.8845007609964805
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b>: Clinical manifestations and diagnosis in children",
                "url": "https://www.uptodate.com/contents/covid-19-clinical-manifestations-and-diagnosis-in-children?search=covid+19&source=search_result&selectedTitle=4%7E150&usage_type=default&display_rank=4",
                "source": "uptodate",
                "date": "2021-11-27T02:37:02.279208",
                "author": "",
                "abstract": "",
                "score": 0.6821202919551691
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b>: Vaccines to prevent SARS-CoV-2 infection",
                "url": "https://www.uptodate.com/contents/covid-19-vaccines-to-prevent-sars-cov-2-infection?search=covid+19&source=search_result&selectedTitle=6%7E150&usage_type=default&display_rank=6",
                "source": "uptodate",
                "date": "2021-11-27T02:37:02.280213",
                "author": "",
                "abstract": "",
                "score": 0.5826949833240135
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b>: Outpatient evaluation and management of acute illness in adults",
                "url": "https://www.uptodate.com/contents/covid-19-outpatient-evaluation-and-management-of-acute-illness-in-adults?search=covid+19&source=search_result&selectedTitle=2%7E150&usage_type=default&display_rank=2",
                "source": "uptodate",
                "date": "2021-11-27T02:37:02.279208",
                "author": "",
                "abstract": "",
                "score": 0.3864737907347551
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b>: Evaluation and management of adults following acute viral illness",
                "url": "https://www.uptodate.com/contents/covid-19-evaluation-and-management-of-adults-following-acute-viral-illness?search=covid+19&source=search_result&selectedTitle=8%7E150&usage_type=default&display_rank=8",
                "source": "uptodate",
                "date": "2021-11-27T02:37:02.280213",
                "author": "",
                "abstract": "",
                "score": 0.3864737907347551
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b>: Risks for infection, clinical presentation, testing, and approach to infected patients with cancer",
                "url": "https://www.uptodate.com/contents/covid-19-risks-for-infection-clinical-presentation-testing-and-approach-to-infected-patients-with-cancer?search=covid+19&source=search_result&selectedTitle=9%7E150&usage_type=default&display_rank=9",
                "source": "uptodate",
                "date": "2021-11-27T02:37:02.280213",
                "author": "",
                "abstract": "",
                "score": 0.06
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b> and Cardiovascular Disease Patients",
                "url": "https://www.dynamed.com/condition/covid-19-and-cardiovascular-disease-patients",
                "source": "dynamed",
                "date": "2021-11-27T02:37:03.046517",
                "author": "",
                "abstract": "",
                "score": 1.0
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b> and Pregnant Patients",
                "url": "https://www.dynamed.com/condition/covid-19-and-pregnant-patients",
                "source": "dynamed",
                "date": "2021-11-27T02:37:03.046517",
                "author": "",
                "abstract": "",
                "score": 0.9721937201503069
            },
            {
                "title": "Management of <b><b>covid</b></b>-<b><b>19</b></b>",
                "url": "https://www.dynamed.com/management/management-of-covid-19",
                "source": "dynamed",
                "date": "2021-11-27T02:37:03.046517",
                "author": "",
                "abstract": "",
                "score": 0.9167156444157845
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b> and Patients With Cancer",
                "url": "https://www.dynamed.com/management/covid-19-and-patients-with-cancer",
                "source": "dynamed",
                "date": "2021-11-27T02:37:03.046517",
                "author": "",
                "abstract": "",
                "score": 0.8661893630281452
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b> and Special Populations",
                "url": "https://www.dynamed.com/condition/covid-19-and-special-populations",
                "source": "dynamed",
                "date": "2021-11-27T02:37:03.046517",
                "author": "",
                "abstract": "",
                "score": 0.8661893630281452
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b> and Pediatric Patients",
                "url": "https://www.dynamed.com/condition/covid-19-and-pediatric-patients",
                "source": "dynamed",
                "date": "2021-11-27T02:37:03.046517",
                "author": "",
                "abstract": "",
                "score": 0.8661893630281452
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b> (Novel Coronavirus)",
                "url": "https://www.dynamed.com/condition/covid-19-novel-coronavirus",
                "source": "dynamed",
                "date": "2021-11-27T02:37:03.045517",
                "author": "",
                "abstract": "",
                "score": 0.06601276258088928
            },
            {
                "title": "SARS-COV-2 (<b><b>covid</b></b>-<b><b>19</b></b>) Vaccine, mRNA (Pfizer)",
                "url": "https://www.dynamed.com/drug-monograph/sars-cov-2-covid-19-vaccine-mrna-pfizer",
                "source": "dynamed",
                "date": "2021-11-27T02:37:03.046517",
                "author": "",
                "abstract": "",
                "score": 0.019002514309338168
            },
            {
                "title": "SARS-COV-2 (<b><b>covid</b></b>-<b><b>19</b></b>) Vaccine, mRNA (Moderna)",
                "url": "https://www.dynamed.com/drug-monograph/sars-cov-2-covid-19-vaccine-mrna-moderna",
                "source": "dynamed",
                "date": "2021-11-27T02:37:03.046517",
                "author": "",
                "abstract": "",
                "score": 0.019002514309338168
            },
            {
                "title": "SARS-COV-2 (<b><b>covid</b></b>-<b><b>19</b></b>) Vaccine, Adenovirus 26 Vector (Janssen)",
                "url": "https://www.dynamed.com/drug-monograph/sars-cov-2-covid-19-vaccine-adenovirus-26-vector-janssen",
                "source": "dynamed",
                "date": "2021-11-27T02:37:03.046517",
                "author": "",
                "abstract": "",
                "score": 0.05
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b> antibody testing - Mayo Clinic",
                "url": "https://www.mayoclinic.org/tests-procedures/covid-19-antibody-testing/about/pac-20489696",
                "source": "mayoclinic",
                "date": "2021-11-27T02:37:17.981425",
                "author": "",
                "abstract": "",
                "score": 1.0
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b> diagnostic testing - Mayo Clinic",
                "url": "https://www.mayoclinic.org/tests-procedures/covid-19-diagnostic-test/about/pac-20488900",
                "source": "mayoclinic",
                "date": "2021-11-27T02:37:17.982425",
                "author": "",
                "abstract": "",
                "score": 1.0
            },
            {
                "title": "Coronavirus disease 20<b><b>19</b></b> (<b><b>covid</b></b>-<b><b>19</b></b>) - Symptoms and causes - Mayo Clinic",
                "url": "https://www.mayoclinic.org/diseases-conditions/coronavirus/symptoms-causes/syc-20479963",
                "source": "mayoclinic",
                "date": "2021-11-27T02:37:17.981425",
                "author": "",
                "abstract": "",
                "score": 0.9772030062974035
            },
            {
                "title": "<b><b>covid</b></b>-<b><b>19</b></b> (coronavirus) travel advice - Mayo Clinic",
                "url": "https://www.mayoclinic.org/diseases-conditions/coronavirus/in-depth/coronavirus-safe-travel-advice/art-20486965",
                "source": "mayoclinic",
                "date": "2021-11-27T02:37:17.982425",
                "author": "",
                "abstract": "",
                "score": 0.9699244211248723
            },
            {
                "title": "Get the facts about <b><b>covid</b></b>-<b><b>19</b></b> vaccines - Mayo Clinic",
                "url": "https://www.mayoclinic.org/diseases-conditions/coronavirus/in-depth/coronavirus-vaccine/art-20484859",
                "source": "mayoclinic",
                "date": "2021-11-27T02:37:17.982425",
                "author": "",
                "abstract": "",
                "score": 0.9138851940798917
            },
            {
                "title": "Pregnancy and <b><b>covid</b></b>-<b><b>19</b></b>: What are the risks? - Mayo Clinic",
                "url": "https://www.mayoclinic.org/diseases-conditions/coronavirus/in-depth/pregnancy-and-covid-19/art-20482639",
                "source": "mayoclinic",
                "date": "2021-11-27T02:37:17.982425",
                "author": "",
                "abstract": "",
                "score": 0.8877283774327106
            },
            {
                "title": "How does <b><b>covid</b></b>-<b><b>19</b></b> affect people with diabetes? - Mayo Clinic",
                "url": "https://www.mayoclinic.org/diseases-conditions/coronavirus/multimedia/how-does-covid-19-affect-people-with-diabetes/vid-20510584",
                "source": "mayoclinic",
                "date": "2021-11-27T02:37:17.982425",
                "author": "",
                "abstract": "",
                "score": 0.8877283774327106
            },
            {
                "title": "Different types of <b><b>covid</b></b>-<b><b>19</b></b> vaccines: How they work - Mayo Clinic",
                "url": "https://www.mayoclinic.org/diseases-conditions/coronavirus/in-depth/different-types-of-covid-19-vaccines/art-20506465",
                "source": "mayoclinic",
                "date": "2021-11-27T02:37:17.982425",
                "author": "",
                "abstract": "",
                "score": 0.8627005877127333
            },
            {
                "title": "Multisystem inflammatory syndrome in children (MIS-C) and <b><b>covid</b></b>-<b><b>19</b></b> - Symptoms and causes - Mayo Clinic",
                "url": "https://www.mayoclinic.org/diseases-conditions/mis-c-in-kids-covid-19/symptoms-causes/syc-20502550",
                "source": "mayoclinic",
                "date": "2021-11-27T02:37:17.981425",
                "author": "",
                "abstract": "",
                "score": 0.7724729801694035
            },
            {
                "title": "Coronavirus - Symptoms and causes",
                "url": "https://www.mayoclinic.org/diseases-conditions/coronavirus/symptoms-causes/syc-20479963",
                "source": "mayoclinic",
                "date": "2021-11-27T02:37:17.981425",
                "author": "",
                "abstract": "",
                "score": 0.05
            }
        ],
        "search_stats": {
            "uptodate": {
                "time": "11.52",
                "number_of_results": 10
            },
            "dynamed": {
                "time": "12.03",
                "number_of_results": 10
            },
            "mayoclinic": {
                "time": "26.97",
                "number_of_results": 10
            }
        }
    }
    return response

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8001)