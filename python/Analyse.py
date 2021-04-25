import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 100)


class Analyse:

    def laenge(self, dff):
        # ratings = pd.read_csv('cleaned_ratings.csv')
        # movies = pd.read_csv('cleaned_movies.csv')
        movies = dff
        movies = movies[(movies['duration'] >= 0) & (movies['avg_vote'] >= 0)][
            ['title', 'duration', 'avg_vote', 'year', 'votes']]
        counts = movies.groupby('duration').agg(
            {'title': 'count', 'avg_vote': ['mean', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)],
             'votes': 'sum'})

        counts = counts[counts['title']['count'] >= 10]

        counts['avg_vote_mean'] = counts['avg_vote']['mean']
        counts['avg_vote_25pct'] = counts['avg_vote']['<lambda_0>']
        counts['avg_vote_75pct'] = counts['avg_vote']['<lambda_1>']
        counts['title_counts'] = counts['title']['count']
        counts['votes_sum'] = counts['votes']['sum']
        del counts['avg_vote']
        del counts['title']

        """
        fig, ax = plt.subplots(2, 1, sharex=True)
        ax[0].plot(counts.index, counts['avg_vote_mean'], color="b")
        ax[0].plot(counts.index, counts['avg_vote_25pct'], color="r", alpha=0.5)
        ax[0].plot(counts.index, counts['avg_vote_75pct'], color="g", alpha=0.5)
        ax[1].bar(counts.index, counts['title_counts'])
        plt.show()
        return plt.gcf()
        """
        return counts

    def get_genres(self):
        movies = pd.read_csv('cleaned_movies.csv')
        genres = movies[movies['genre'] != "UNKNOWN"]['genre']
        genre_unique = genres.unique()
        genre_list = []
        for genre in genre_unique:
            a = genre.split(",")
            for i in a:
                t = i.strip()
                if t in genre_list:
                    pass
                else:
                    genre_list.append(t)

        return genre_list

    def test_str(self, genres_list):
        movies = pd.read_csv('cleaned_movies.csv')
        if not genres_list:
            return movies
        else:
            gen_str = ""
            for i in range(len(genres_list)):
                if i == len(genres_list) - 1:
                    gen_str += genres_list[i]
                else:
                    gen_str += genres_list[i] + "|"

            movies_filterd = movies[movies['genre'].str.contains(gen_str)]
            return movies_filterd

    def votesByRating(self):
        movies = pd.read_csv('cleaned_movies.csv')
        movies2 = movies[(movies['votes'] >= 0) & (movies['avg_vote'] >= 0)][['title', 'votes', 'avg_vote']]
        counts = movies2.groupby('avg_vote').agg(
            {'title': 'count', 'votes': ['mean', lambda x: x.quantile(0.50), lambda x: x.quantile(0.75)]})
        counts = counts[counts['title']['count'] >= 10]

        counts['votes_mean'] = counts['votes']['mean']
        counts['votes_25pct'] = counts['votes']['<lambda_0>']
        counts['votes_75pct'] = counts['votes']['<lambda_1>']
        counts['title_counts'] = counts['title']['count']

        fig, ax = plt.subplots(2, 1, sharex=True)
        ax[0].plot(counts.index, counts['votes_mean'], color="b")
        ax[0].plot(counts.index, counts['votes_25pct'], color="r", alpha=0.5)
        # ax[0].plot(counts.index, counts['votes_75pct'], color="g", alpha=0.5)
        ax[1].bar(counts.index, counts['title_counts'])
        plt.show()

    def votesByRating_dash(self):
        movies = pd.read_csv('cleaned_movies.csv')
        movies2 = movies[(movies['votes'] >= 0) & (movies['avg_vote'] >= 0)][['title', 'votes', 'avg_vote']]
        counts = movies2.groupby('avg_vote').agg(
            {'title': 'count', 'votes': ['mean', lambda x: x.quantile(1), lambda x: x.quantile(0.50)]})
        counts = counts[counts['title']['count'] >= 10]

        counts['votes_mean'] = counts['votes']['mean']
        counts['votes_100pct'] = counts['votes']['<lambda_0>']
        counts['votes_median'] = counts['votes']['<lambda_1>']
        counts['title_counts'] = counts['title']['count']
        return counts

    def gender_support(self, dataframe, genres_list):
        movies = dataframe
        if genres_list == []:
            return movies
        else:
            gen_str = ""
            for i in range(len(genres_list)):
                if i == len(genres_list) - 1:
                    gen_str += genres_list[i]
                else:
                    gen_str += genres_list[i] + "|"

            movies_filterd = movies[movies['genre'].str.contains(gen_str)]
            movies_filterd.loc[:, 'genre'] = gen_str
            return movies_filterd

    def gender(self):
        rating = pd.read_csv('cleaned_ratings.csv')
        movie = pd.read_csv('cleaned_movies.csv')
        rating_int = rating[(rating['males_allages_avg_vote'] >= 0) & (rating['females_allages_avg_vote'] >= 0)][[
            'imdb_title_id', 'males_allages_avg_vote', 'males_allages_votes', 'females_allages_avg_vote',
            'females_allages_votes']]
        movie_int = movie[movie['genre'] != "UNKNOWN"][['imdb_title_id', 'title', 'genre']]

        merged_df = movie_int.merge(rating_int, how="inner", on='imdb_title_id')

        genres_list = self.get_genres()
        complete_dff = pd.DataFrame()

        for genre in genres_list:
            dff = self.gender_support(merged_df, [genre])
            complete_dff = pd.concat([complete_dff, dff], ignore_index=True)

        counts = complete_dff.groupby('genre').agg({'title': 'count', 'males_allages_avg_vote': 'mean',
                                                    'females_allages_avg_vote': 'mean', 'males_allages_votes': 'mean',
                                                    'females_allages_votes': 'mean'})
        print(counts.head(20))

        counts = counts[counts['title'] >= 10]

        counts['m_avg'] = counts['males_allages_avg_vote']
        counts['f_avg'] = counts['females_allages_avg_vote']
        counts['f_vote'] = counts['females_allages_votes']
        counts['m_vote'] = counts['males_allages_votes']

        index = np.arange(counts.index.size)
        w = 0.4

        fig, ax = plt.subplots(2, 1, sharex=True)
        ax[0].bar(index + w, counts['m_avg'], color="b", width=w, align='center')
        ax[0].bar(index, counts['f_avg'], color="r", width=w, align='center')
        ax[1].bar(index, counts['f_vote'], color="r", width=w, align='center')
        ax[1].bar(index + w, counts['m_vote'], color="b", width=w, align='center')
        plt.xticks(index + w / 2, counts.index, rotation=90, horizontalalignment='center')
        plt.show()

    def gender_dash(self):
        rating = pd.read_csv('cleaned_ratings.csv')
        movie = pd.read_csv('cleaned_movies.csv')
        rating_int = rating[(rating['males_allages_avg_vote'] >= 0) & (rating['females_allages_avg_vote'] >= 0)][
            ['imdb_title_id', 'males_allages_avg_vote', 'males_allages_votes', 'females_allages_avg_vote',
             'females_allages_votes']]

        movie_int = movie[movie['genre'] != "UNKNOWN"][['imdb_title_id', 'title', 'genre']]
        merged_df = movie_int.merge(rating_int, how="inner", on='imdb_title_id')

        genres_list = self.get_genres()
        complete_dff = pd.DataFrame()

        for genre in genres_list:
            dff = self.gender_support(merged_df, [genre])
            complete_dff = pd.concat([complete_dff, dff], ignore_index=True)

        counts = complete_dff.groupby('genre').agg(
            {'title': 'count', 'males_allages_avg_vote': 'mean', 'females_allages_avg_vote': 'mean',
             'males_allages_votes': 'mean', 'females_allages_votes': 'mean'})

        counts = counts[counts['title'] >= 10]

        counts['m_avg'] = counts['males_allages_avg_vote']
        counts['f_avg'] = counts['females_allages_avg_vote']
        counts['f_vote'] = counts['females_allages_votes']
        counts['m_vote'] = counts['males_allages_votes']

        return counts

    def stars(self):
        fakten = pd.read_csv('cleaned_fakten.csv')
        rating = pd.read_csv('cleaned_ratings.csv')

        filtered_fakten = fakten[(fakten['category'] == "actress") | (fakten['category'] == "actor")]
        group = filtered_fakten.groupby('imdb_title_id').agg({'imdb_name_id': 'count'})

        ratingfilt = rating[['imdb_title_id', 'mean_vote']]
        joined = group.merge(ratingfilt, how="inner", left_index=True, right_on='imdb_title_id')
        joinedgroup = joined.groupby('imdb_name_id').agg({'mean_vote': ['mean', lambda x: x.quantile(0.25),
                                                                        lambda x: x.quantile(0.75)],
                                                          'imdb_title_id': 'count'})

        groupact = filtered_fakten.groupby(['imdb_title_id', 'category']).agg({'imdb_name_id': 'count'})

        normal = groupact.reset_index(level='category')
        pivot = normal.pivot_table('imdb_name_id', ['imdb_title_id'], 'category')
        pivot = pivot.fillna(0)
        pivot['mw_quota'] = pivot['actress'] / (pivot['actor'] + pivot['actress'])
        piv_rat = pivot.merge(rating, how='inner', on='imdb_title_id')

        return joinedgroup, piv_rat


if __name__ == "__main__":
    a = Analyse()
    # movies = pd.read_csv('cleaned_movies.csv')
    a.stars()
