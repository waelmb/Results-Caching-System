import pandas as pd
import numpy as np
import sklearn
from sklearn.decomposition import LatentDirichletAllocation
import nltk
import yake
import collections
from collections import Counter
import glob
import csv
import spacy
import en_core_sci_sm

def get_trending_topics(documents):
    df = pd.DataFrame({'All_docs' : documents})
    df[1] = df['All_docs'].str.lower().str.replace('[^\w\s]', ' ').str.replace(' +', ' ').str.strip()
    df[1] = df.apply(lambda row: nltk.word_tokenize(row[1]), axis=1)
    df[1] = df[1].apply(lambda f: [nltk.WordNetLemmatizer().lemmatize(word) for word in f])
    count_v = sklearn.feature_extraction.text.CountVectorizer(analyzer = 'word', ngram_range = (1, 2))
    raw_documents = []
    for i, r in df.iterrows():
        raw_documents.append(", ".join(r[1]))
    vects = count_v.fit_transform(raw_documents)
    
    lda_m = LatentDirichletAllocation(n_components = 10, random_state = 10, evaluate_every = -1, n_jobs = -1,)
    real_lda = lda_m.fit_transform(vects)
    topic_name_lst = ["Topic" + str(i) for i in range(1, lda_m.n_components + 1)]
    doc_tops = pd.DataFrame(np.round(real_lda, 2), columns = topic_name_lst)
    dom_top = (np.argmax(doc_tops.values, axis = 1) + 1)
    doc_tops['Dominant_topic'] = dom_top
    df = pd.merge(df, doc_tops, left_index = True, right_index = True, how = 'outer')
    main_words = np.array(count_v.get_feature_names())
    
    full_topics = []
    for weights in lda_m.components_:
        top_locs = (-weights).argsort()[ : 20]
        full_topics.append(main_words.take(top_locs))
    
    duplicates = []
    for top in full_topics:
        for word in top:
            duplicates.append(str(word))
    duplicates = [i for i, c in collections.Counter(duplicates).items() if c > 1]
    
    refined_topics = []
    for top in full_topics:
        top_without_dups = []
        for word in top:
            if str(word) not in duplicates:
                top_without_dups.append(str(word))
        refined_topics.append(top_without_dups)
        
    df_refined_topics = pd.DataFrame(refined_topics)
    df_refined_topics.columns = ['Term '+ str(i) for i in range(1, df_refined_topics.shape[1] + 1)]
    df_refined_topics['Topic_keywords'] = df_refined_topics.values.tolist()
    df_refined_topics['Topic_number'] = df_refined_topics.index + 1
    df_refined_topics = df_refined_topics[['Topic_keywords', 'Topic_number']]
    
    tops = []
    for top in df_refined_topics['Topic_keywords']:
        tops.append([i for i in top if i is not None])
    df_refined_topics['Topic_keywords'] = tops
    df = pd.merge(df, df_refined_topics, left_on = 'Dominant_topic', right_on = 'Topic_number')
    del df['Topic_number']
    
    lst_of_top_nums = df['Dominant_topic'].tolist()
    t = Counter(lst_of_top_nums).most_common(3)
    trending = []
    for pair in t:
        trending.append(pair[0])
    
    trending_topics = []
    for num in trending:
        trending_topics.append(refined_topics[num - 1])
    final_trending_topics = []
    for top in trending_topics:
        final_trending_topics.append(' '.join(top))
    
    relevant_docs = df.loc[df['Dominant_topic'].isin(trending), 'All_docs']
    
    all_relevant_docs = ' '.join(relevant_docs)
    custom_kw_extractor = yake.KeywordExtractor(lan = "en", n = 3, dedupLim = 0.9, top = 20, features = None)
    keywords = custom_kw_extractor.extract_keywords(all_relevant_docs)
    trending_topics_yake = []
    for pair in keywords:
        trending_topics_yake.append(pair[0])
    nlp = spacy.load("en_core_sci_sm")
    trending_topics_yake_all = ' '.join(trending_topics_yake)
    doc = nlp(trending_topics_yake_all)
    entities = list(doc.ents)
    str_ents = []
    for ents in entities:
        str_ents.append(str(ents))
    final_trending_topics_yake = []
    for top in trending_topics_yake:
        if not any(top in ent for ent in str_ents):
            final_trending_topics_yake.append(top)
    trends = final_trending_topics + final_trending_topics_yake
    return trends

read_files = glob.glob('articles/*')
with open("articles.csv", "w") as outfile:
    w = csv.writer(outfile)
    for f in read_files:
        with open(f, "r") as infile:
            w.writerow([" ".join([line.strip() for line in infile])])

data = pd.read_csv("articles.csv", header=None)
input = data[0].tolist()
trends = get_trending_topics(input)
print(trends)
