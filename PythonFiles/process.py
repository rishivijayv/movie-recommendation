# This file converts the original "tmdb_5000" data from kaggle into data that can be used
# for recommendation. Involves joining tables with movie metadata(crew, cast etc) and movie information
# into one. New data is written to a .csv file and then read when using the program. This file is only run once
# to create the "movie_data.csv" file.

import numpy as np
import pandas as pd
from ast import literal_eval

df1 = pd.read_csv(r'C:\Users\rishi_rhvenli\PycharmProjects\MovieRec\Data\tmdb_5000_credits.csv')
df2 = pd.read_csv(r'C:\Users\rishi_rhvenli\PycharmProjects\MovieRec\Data\tmdb_5000_movies.csv')
df1.columns = ['id', 'title', 'cast', 'crew']

# Merge the 2 dataframes by movie-id
df2= df2.merge(df1, on='id')

df2['overview'] = df2['overview'].fillna('')

features = ['cast', 'crew', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(literal_eval)


# Extract the director from the crew-list
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan


# Used to extract top-4 items in a list (eg: top 4 cast members in a movie)
def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        if len(names) > 4:
            names = names[:4]
        return names
    return []


# Extracts the director and other meta-information from the dataframe
df2['director'] = df2['crew'].apply(get_director)
features = ['cast', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(get_list)


# Converts data in 'x' to lower case and removes all spaces.
# Done to differentiate, for example, Chris Pratt from Chris Evans
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''


# Cleans the data in the newly made columns
features = ['cast', 'director', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(clean_data)
df2['new_title'] = df2['original_title'].apply(clean_data)


# Creates a 'soup' of information that can be used to check for 'similar' movies
def create_soup(x):
    return ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])


df2['soup'] = df2.apply(create_soup, axis=1)
df2.to_csv(r'C:\Users\rishi_rhvenli\PycharmProjects\MovieRec\Data\movie_data.csv', index=None, header=True)
# DATA PROCESSING ENDS

