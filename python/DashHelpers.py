import dash_bootstrap_components as dbc
import dash_html_components as html
import json
import requests

API_KEY = "fd8b017cb08c608a532146943f5b2113"

def durationDrop():
    # future automate with select genres
    genres = ["Romance", 'Biography', 'Crime', 'History', 'Adventure', 'Fantasy', 'War', 'Mystery', 'Horror',
              'Western', 'Comedy', 'Family', 'Action', 'Sci-Fi', 'Thriller', 'Sport', 'Animation', 'Musical',
              'Music', 'Film-Noir']

    l = []
    for i in genres:
        l.append({"label": i, "value": i})
    return l

def topDrop():
    # future automate with select genres
    genres = ["Romance", 'Biography', 'Crime', 'History', 'Adventure', 'Fantasy', 'War', 'Mystery', 'Horror',
              'Western', 'Comedy', 'Family', 'Action', 'Sci-Fi', 'Thriller', 'Sport', 'Animation', 'Musical',
              'Music', 'Film-Noir', 'Adult', 'Documentary', 'Reality-TV', 'News']

    l = []
    for i in genres:
        l.append({"label": i, "value": i})

    return l

def topResult(df):
    l = []
    image_list = tmdbApiPic(df)
    NO_IMAGE = "/assets/no_picture.png"

    for i in range(len(df)):

        if image_list[i]:
            if image_list[i][0]:
                titel = image_list[i][0]
            else:
                titel = df.iloc[i, 1]
            if image_list[i][1]:
                image = image_list[i][1]
            else:
                image = NO_IMAGE
        else:
            titel = df.iloc[i, 1]
            image = NO_IMAGE

        l.append(dbc.Col([
                html.Img(src=image, width="150px"),
                html.Plaintext(titel + "\nRating: " + str(df.iloc[i, 2]) + "\n" + str(df.iloc[i, 3]) + " Votes"),
            ]))
    while len(l) < 10:
        l.append(dbc.Col([
                html.Img(src="/assets/no_movie.png", width="150px"),
                html.Plaintext("No Movie, sry xD"),
            ]))

    return [dbc.Row(l[:5]), dbc.Row(l[5:])]


def tmdbApiPic(df):
    topstr = "https://image.tmdb.org/t/p/w200"
    topstr2 = "https://api.themoviedb.org/3/find/"
    bottomstr = "?api_key=" + API_KEY + "&language=en-US&external_source=imdb_id"

    l = []

    for i in range(len(df)):
        imdbid = df.iloc[i, 0]
        build = topstr2 + imdbid + bottomstr
        response = requests.get(build).text
        respJSON = json.loads(response)
        if respJSON['movie_results']:
            title = respJSON['movie_results'][0]['title']
            if respJSON['movie_results'][0]['poster_path']:
                poster = topstr + respJSON['movie_results'][0]['poster_path']
            else:
                poster = None
            l.append([title, poster])
        else:
            l.append(None)

    return l

