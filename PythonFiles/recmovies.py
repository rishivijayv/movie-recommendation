from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Read the data from the newly created .csv file into a dataframe
df = pd.read_csv(r'C:\Users\rishi_rhvenli\PycharmProjects\MovieRec\Data\movie_data.csv')

# Similarity Matrix for Overview Recommendations
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['overview'].values.astype('U'))
overview_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Similarity Matrix for Metadata recommendations
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df['soup'])
meta_matrix = cosine_similarity(count_matrix, count_matrix)
df = df.reset_index()
# Creates a reverse-mapping that gives index of movie given its title
indices = pd.Series(df.index, index=df['new_title']).drop_duplicates()


# Recommends 10 movies with similar plotline or crew.
def recommend(title, matrix=overview_matrix):
    idx = indices[title]
    sim_scores = list(enumerate(matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df['original_title'].loc[movie_indices]

