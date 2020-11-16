import pandas as pd
import numpy as np
import pickle
import datetime as dt
from sklearn.metrics.pairwise import cosine_similarity


#Function to get articles closest in topic/subtopic/date published to input article
def get_recs(article_index, n = 5, topic_df = None, dists = None):


    topic_weights = topic_df[['Neuroscience/ Behavioral Sci.', 'Astronomy',
           'Climate Science', 'Diseases/ Epidemics/ Viruses',
           'Optics/ Electronics/ Photonics/ Device Physics',
           'Drug Discovery/ Pharmaceuticals',
           'Genetics/Genomics', 'Ocean Sciences/ Geology', 
           'Stem Cells/ Cloning', 'Agriculture/ Plant Sciences',
           'Cellular Bio./ Molecular Bio.', 'Evolution/ Archaeology',
           'Phyics/ Particle Physics/ Quantum Physics',
           'Space Travel/ Exploration', 'Wildlife/ Conservation/ Biodiversity',
           'Planetary Science/ Solar System']]
    dists = cosine_similarity(topic_weights)
    
    

    print(topic_df.loc[article_index, 'title'])

    top = np.argsort(dists[article_index])[-2::-1]
    count = 0
    recs = []
    start = 0
    stop = 100
    while count < n:
        for ind in top[start:stop]:
            if set(topic_df.loc[article_index, 'all_topics']) & set(topic_df.loc[ind, 'all_topics']):
                if topic_df.loc[article_index, 'subtopic'] == topic_df.loc[ind, 'subtopic']:
                    if topic_df.loc[article_index, 'year'] == topic_df.loc[ind, 'year']:
                        count+=1
                        print(topic_df.loc[ind, 'subtopic'], topic_df.loc[ind, 'year'])
                        if count == n:
                            break

                        recs.append(ind)
        if count == n:
            break

        for ind in top[start:stop]:
            if set(topic_df.loc[article_index, 'all_topics']) & set(topic_df.loc[ind, 'all_topics']):
                if topic_df.loc[article_index, 'subtopic'] == topic_df.loc[ind, 'subtopic']:
                    if topic_df.loc[article_index, 'year'] != topic_df.loc[ind, 'year']:

                        count+=1
                        if count == n:
                            break
                        print(topic_df.loc[ind, 'subtopic'], topic_df.loc[ind, 'year'])
                        recs.append(ind)
        if count ==n:
            break
        for ind in top[start:stop]:
            if set(topic_df.loc[article_index, 'all_topics']) & set(topic_df.loc[ind, 'all_topics']):
                if topic_df.loc[article_index, 'subtopic'] != topic_df.loc[ind, 'subtopic']:
                    if topic_df.loc[article_index, 'year'] == topic_df.loc[ind, 'year']:

                        count+=1
                        print(topic_df.loc[ind, 'subtopic'], topic_df.loc[ind, 'year'])
                        if count == n:
                            break
                        recs.append(ind)
        if count == n:
            break

        for ind in top[start:stop]:
            if set(topic_df.loc[article_index, 'all_topics']) & set(topic_df.loc[ind, 'all_topics']):
                if topic_df.loc[article_index, 'subtopic'] != topic_df.loc[ind, 'subtopic']:
                    if topic_df.loc[article_index, 'year'] != topic_df.loc[ind, 'year']:

                        count+=1
                        print(topic_df.loc[ind, 'subtopic'], topic_df.loc[ind, 'year'])
                        if count == n:
                            break
                        recs.append(ind)
        start +=50
        stop +=50


    print('\nRecs:\n')
    
    title_list = []
    url_list = []
    for rec in recs:
        title_list.append(topic_df.loc[rec, 'title'])
        url_list.append(topic_df.loc[rec, 'url'])
        print(topic_df.loc[rec, 'title'])
    return recs, title_list, url_list    


#Load topic/subtopic dataframe, calculate cosine similarity matrix
def get_df_and_dists():
    topic_df = pickle.load(open('subtopic_df', 'rb'))
    topic_df.reset_index(inplace=True)
    
    topic_weights = topic_df[['Neuroscience/ Behavioral Sci.', 'Astronomy',
           'Climate Science', 'Diseases/ Epidemics/ Viruses',
           'Optics/ Electronics/ Photonics/ Device Physics',
           'Drug Discovery/ Pharmaceuticals',
           'Genetics/Genomics', 'Ocean Sciences/ Geology', 
           'Stem Cells/ Cloning', 'Agriculture/ Plant Sciences',
           'Cellular Bio./ Molecular Bio.', 'Evolution/ Archaeology',
           'Phyics/ Particle Physics/ Quantum Physics',
           'Space Travel/ Exploration', 'Wildlife/ Conservation/ Biodiversity',
           'Planetary Science/ Solar System']]
    
    dists = cosine_similarity(topic_weights)
    
    return topic_df, dists

#Load and return topic/subtopic dataframe
def get_df():
    topic_df = pickle.load(open('subtopic_df', 'rb'))
    topic_df.reset_index(inplace=True)
    
    return topic_df