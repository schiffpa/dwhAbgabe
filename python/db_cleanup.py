import pandas as pd
import pymongo
from pymongo import MongoClient
from datetime import datetime


"""transform .csv data"""
def personen_db():
    personen = pd.read_csv("imdb_names.csv")
    del personen['spouses_with_children']
    del personen['spouses_string']
    del personen['death_details']
    del personen['birth_details']
    del personen['bio']
    del personen['birth_name']

    personen['height'] = personen['height'].fillna(-1.0)
    personen = personen.fillna("UNKNOWN")
    personen.to_csv("cleaned_personen.csv", index = False)


def ratings_db():
    ratings = pd.read_csv("imdb_ratings.csv")
    del ratings['top1000_voters_rating']
    del ratings['top1000_voters_votes']
    ratings = ratings.fillna(-1)
    ratings.to_csv("cleaned_ratings.csv", index = False)


def movies_db():
    movies = pd.read_csv("imdb_movies.csv")
    del movies['description']
    del movies['actors']

    movies['budget_currency'] = movies.budget.str.split(" ").str[0]
    movies['budget_value'] = movies.budget.str.split(" ").str[-1]
    movies['budget_currency'] = movies['budget_currency'].fillna("UNKNOWN")
    movies['budget_value'] = movies['budget_value'].fillna(-1)
    del movies['budget']

    movies['usa_gross_income_currency'] = movies.usa_gross_income.str.split(" ").str[0]
    movies['usa_gross_income_value'] = movies.usa_gross_income.str.split(" ").str[-1]
    movies['usa_gross_income_value'] = movies['usa_gross_income_value'].fillna(-1)
    movies['usa_gross_income_currency'] = movies['usa_gross_income_currency'].fillna("UNKNOWN")
    del movies['usa_gross_income']

    movies['worlwide_gross_income_currency'] = movies.worlwide_gross_income.str.split(" ").str[0]
    movies['worlwide_gross_income_value'] = movies.worlwide_gross_income.str.split(" ").str[-1]
    movies['worlwide_gross_income_value'] = movies['worlwide_gross_income_value'].fillna(-1)
    movies['worlwide_gross_income_currency'] = movies['worlwide_gross_income_currency'].fillna("UNKNOWN")
    del movies['worlwide_gross_income']

    movies['metascore'] = movies['metascore'].fillna(-1)
    movies['reviews_from_users'] = movies['reviews_from_users'].fillna(-1)
    movies['reviews_from_critics'] = movies['reviews_from_critics'].fillna(-1)

    movies = movies.fillna("UNKNOWN")

    movies.to_csv("cleaned_movies.csv", index = False)

def fakten_db():
    fakten = pd.read_csv("imdb_title_principals.csv")
    del fakten['ordering']
    del fakten['job']
    del fakten['characters']
    fakten.to_csv("cleaned_fakten.csv", index = False)

def clean_dbs():
    movies_db()
    fakten_db()
    personen_db()
    ratings_db()


"""load to and from Mongo Cloud"""
def load_To_Mongo():
    moviesdf = pd.read_csv("cleaned_movies.csv")
    personendf = pd.read_csv("cleaned_personen.csv")
    faktendf = pd.read_csv("cleaned_fakten.csv")
    ratingsdf = pd.read_csv("cleaned_ratings.csv")

    dfs = [moviesdf, personendf, faktendf, ratingsdf]
    mongoColec = ["Movies", "Personen", "Fakten", "Ratings"]

    client = MongoClient("mongodb+srv://XXX:YYYYYYY@movies.6kuoq.mongodb.net/Movies?retryWrites=true&w=majority")
    #Todo insert credentials
    db = client["Movies"]

    if len(dfs) == len(mongoColec):
        for i in range(len(dfs)):
            collec = db[mongoColec[i]]
            collec.drop()
            collec.insert_many(dfs[i].to_dict("records"))

def load_from_Mongo(write_to_csv=True):

    client = MongoClient(
        "mongodb+srv://paul:paulhwrdwh@movies.6kuoq.mongodb.net/Movies?retryWrites=true&w=majority")
    db = client["Movies"]

    moviesdf = pd.DataFrame(list(db["Movies"].find()))
    moviesdf = moviesdf.drop(['_id'], axis=1)

    personendf = pd.DataFrame(list(db["Personen"].find()))
    personendf = personendf.drop(['_id'], axis=1)

    ratingsdf = pd.DataFrame(list(db["Ratings"].find()))
    ratingsdf = ratingsdf.drop(['_id'], axis=1)

    faktendf = pd.DataFrame(list(db["Fakten"].find()))
    faktendf = faktendf.drop(['_id'], axis=1)

    if write_to_csv:
        faktendf.to_csv("cleaned_fakten.csv", index=False)
        moviesdf.to_csv("cleaned_movies.csv", index=False)
        ratingsdf.to_csv("cleaned_ratings.csv", index=False)
        personendf.to_csv("cleaned_personen.csv", index=False)

    return moviesdf, personendf, ratingsdf, faktendf

"""load to and from Mongo local"""
def load_To_Mongo_local():
    moviesdf = pd.read_csv("cleaned_movies.csv")
    personendf = pd.read_csv("cleaned_personen.csv")
    faktendf = pd.read_csv("cleaned_fakten.csv")
    ratingsdf = pd.read_csv("cleaned_ratings.csv")

    dfs = [moviesdf, personendf, faktendf, ratingsdf]
    mongoColec = ["Movies", "Personen", "Fakten", "Ratings"]

    client = MongoClient("127.0.0.1:27017")
    db = client["Movies"]

    if len(dfs) == len(mongoColec):
        for i in range(len(dfs)):
            collec = db[mongoColec[i]]
            collec.drop()
            collec.insert_many(dfs[i].to_dict("records"))

def load_from_Mongo_local():

    client = MongoClient("127.0.0.1:27017")
    db = client["Movies"]

    start = datetime.now()

    moviesdf = pd.DataFrame(list(db["Movies"].find()))
    moviesdf = moviesdf.drop(['_id'], axis=1)

    personendf = pd.DataFrame(list(db["Personen"].find()))
    personendf = personendf.drop(['_id'], axis=1)

    ratingsdf = pd.DataFrame(list(db["Ratings"].find()))
    ratingsdf = ratingsdf.drop(['_id'], axis=1)

    faktendf = pd.DataFrame(list(db["Fakten"].find()))
    faktendf = faktendf.drop(['_id'], axis=1)

    end = datetime.now()

    print("Start: ", start)
    print("End: ", end)
    print("Time: ", end - start)

    return moviesdf, personendf, ratingsdf, faktendf

if __name__ == "__main__":
    pass
    #clean_dbs()
    #load_from_Mongo_local()
    #load_from_Mongo()

