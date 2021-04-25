import pandas as pd
import numpy as np
import json
pd.set_option('display.max_columns', 100)

"""Load json Data"""
with open('merged.json', 'r') as myfile:
    data = myfile.read()

jsonstring = json.loads(data)
merged = pd.json_normalize(jsonstring)

"""remove unnecessary datafields"""
merged = merged.drop(['adult', 'backdrop_path', 'belongs_to_collection', 'homepage', 'id', 'overview', 'popularity',
                      'poster_path', 'status', 'tagline', 'video', 'Type', 'DVD', 'BoxOffice', 'Production',
                      'Website', 'Response', '_id.$oid', 'belongs_to_collection.id',
                      'belongs_to_collection.name', 'belongs_to_collection.poster_path', 'Title', 'Released',
                      'belongs_to_collection.backdrop_path', 'revenue.$numberLong', "Rated", "genres", "Plot",
                      "Poster", "spoken_languages", "imdbVotes", "imdbID",
                      "Awards", "Actors", "Language", "Ratings"], axis=1)

"""set TOP1000FLAG"""
movies = pd.read_csv("cleaned_movies.csv")
movies['TOP1000FLAG'] = np.where(movies['imdb_title_id'].isin(merged['imdb_id']), True, False)
missing = merged[~np.where(merged['imdb_id'].isin(movies['imdb_title_id']), True, False)]

"""change TMDB Datastructure to match IMDb"""
# Not implemented

"""check for redundancy and update more up-to-date data"""
# Not implemented

"""rename columns"""
renamed = missing.rename(columns={'imdb_id': 'imdb_title_id', 'title': 'title', 'original_title': 'original_title',
                                  'Year': 'year', 'release_date': 'date_published', 'Genre': 'genre',
                                  'runtime': 'duration', 'Country': 'country', 'original_language': 'language',
                                  'Director': 'director', 'Writer': 'writer',
                                  'production_companies': 'production_company', 'vote_average': 'imdbRating',
                                  'vote_count': 'votes', 'Metascore': 'metascore', 'budget': 'budget_value',
                                  'revenue': 'worlwide_gross_income_value'})

"""fill missing data"""
renamed["worlwide_gross_income_currency"] = "$"
renamed['budget_currency'] = "$"
renamed = renamed.drop(['imdbRating', "Runtime", "production_countries"], axis = 1)
# not finished

"""append to IMDb Data"""
#print(movies.shape)
movies = movies.append(renamed, ignore_index=True)
#print(movies.shape)

"""retun data as json"""
# df.to_json()