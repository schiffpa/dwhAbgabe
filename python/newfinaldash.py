""" imports """
import dash
import dash_core_components as dcc
import plotly.graph_objs as go

from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
from plotly.graph_objs.scatter import Marker

# own creation
import DashHelpers
from Analyse import *
from DashHelpers import *

"""Helper functions"""


def createGenderPlot():
    a = Analyse()
    df = a.gender_dash()
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Average rating per gender and genre", "Average number of votes"))
    fig.append_trace(go.Bar(x=df.index, y=df['f_avg'], marker={'color': "red"}, name="female average rating"), row=1,
                     col=1)
    fig.append_trace(go.Bar(x=df.index, y=df['m_avg'], marker={'color': "blue"}, name="male average rating"), row=1,
                     col=1)
    fig.append_trace(go.Bar(x=df.index, y=df['f_vote'], marker={'color': "darkred"},
                            name="female average number of votes"), row=2, col=1)
    fig.append_trace(go.Bar(x=df.index, y=df['m_vote'], marker={'color': "lightsteelblue"},
                            name="male average number of votes"), row=2, col=1)
    return fig


def createVotesPlot():
    b = Analyse()
    df = b.votesByRating_dash()
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Votes per rating", "Number of movies"),
                        x_title="Rating")
    fig.append_trace(go.Scatter(x=df.index, y=df['votes_mean'], marker=Marker(dict(color="blue")),
                                name="average votes per rating"), row=1, col=1)
    fig.append_trace(go.Scatter(x=df.index, y=df['votes_median'], marker=Marker(dict(color="red")),
                                name="median votes per rating"), row=1, col=1)
    fig.append_trace(go.Scatter(x=df.index, y=df['votes_100pct'], marker=Marker(dict(color="green")),
                                name="most votes per rating"), row=1, col=1)
    fig.append_trace(go.Bar(x=df.index, y=df['title_counts'], marker={'color': "blue"},
                            name="Number of movies with rating x"), row=2, col=1)
    return fig


def createActorsPlotOne():
    b = Analyse()
    comdf, mwdf = b.stars()
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, x_title="Number of stars",
                        subplot_titles=("Average rating", "Number of movies"))
    fig.append_trace(go.Scatter(x=comdf.index, y=comdf['mean_vote']['mean'], name="Average rating"), row=1, col=1)
    fig.append_trace(go.Bar(x=comdf.index, y=comdf['imdb_title_id']['count'], name="Number of movies"), row=2, col=1)

    mwdfgrou = mwdf.groupby('mw_quota').agg({'females_allages_avg_vote': 'mean', 'males_allages_avg_vote': 'mean',
                                             'imdb_title_id': 'count', 'us_voters_rating': 'mean',
                                             'non_us_voters_rating': 'mean'})

    fig2 = make_subplots(rows=3, cols=1, shared_xaxes=True, x_title="Ratio of women", subplot_titles=(
    "Average rating by gender", "Average rating by us and non-us voters", "Number of movies with ratio x"))
    fig2.append_trace(go.Scatter(x=mwdfgrou.index, y=mwdfgrou['females_allages_avg_vote'], marker={'color': "red"},
                                 name="Avg female rating"), row=1, col=1)
    fig2.append_trace(go.Scatter(x=mwdfgrou.index, y=mwdfgrou['males_allages_avg_vote'], marker={'color': "blue"},
                                 name="Avg male rating"), row=1, col=1)
    fig2.append_trace(go.Scatter(x=mwdfgrou.index, y=mwdfgrou['us_voters_rating'], marker={'color': "darkred"},
                                 name="Avg US rating"), row=2, col=1)
    fig2.append_trace(go.Scatter(x=mwdfgrou.index, y=mwdfgrou['non_us_voters_rating'], marker={'color': "steelblue"},
                                 name="Avg Non-US rating"), row=2, col=1)
    fig2.append_trace(go.Bar(x=mwdfgrou.index, y=mwdfgrou['imdb_title_id'], marker={'color': "orange"},
                             name="Ratio of women"), row=3,
                      col=1)
    return fig, fig2


"""Assets"""

LOGO = "/assets/movie_roll.png"

"""App"""

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

"""Style """

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "17rem",
    "padding": "2rem 1rem", }

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    'text-align': 'center'
}

"""Navbar"""

# Navbar dropdown
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("TMDB", href='https://www.themoviedb.org/'),
        dbc.DropdownMenuItem("OMDb", href='https://www.omdbapi.com/'),
        dbc.DropdownMenuItem("IMDB through Kaggle",
                             href='https://www.kaggle.com/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews'),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Project Github", href='https://github.com/schiffpa/dwhAbgabe'),
    ],
    nav=True,
    in_navbar=True,
    label="Data Sources",
)

# Navbar layout
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand(children=[
                            html.H5("Movie Analytics Dashboard"),
                            html.H6("A dissection of the great art of filmmaking")
                        ])),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dropdown,
                    ], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="banner",
)

"""Sidebar"""

sidebar = html.Div(
    [
        html.H2(" ", className="display-4"),
        html.Br(),
        html.Br(),
        html.P(
            "Take a look at some of our charts and analysis", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Top Movies per Genre", href="/page-4", active="exact"),
                dbc.NavLink("Duration", href="/page-1", active="exact"),
                dbc.NavLink("Gender", href="/page-2", active="exact"),
                dbc.NavLink("Votes by Rating", href="/page-3", active="exact"),
                dbc.NavLink("Composition of Stars", href="/page-5", active="exact"),
                dbc.NavLink("TMDB TOP 1000", href="https://dwh.3bute.de", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

"""Content Placeholder"""

content = html.Div(id="page-content", style=CONTENT_STYLE)

"""Apps"""

duration = html.Div([

    html.H1("Movie rating by genre and duration", style={'text-align': 'center'}),
    html.Br(),
    html.Plaintext(
        "We are only considering data points with at least 10 movies per given Genre and Duration to avoid statistical outliers."),
    html.Plaintext(
        "The genre search down below is considered an \"or\" search and will not search for cumulated genres."),

    dcc.Dropdown(
        id="slct_genre",
        options=durationDrop(),
        multi=True,
        placeholder="Select a genre",
        value=[],
        clearable=True,
    ),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_graph', figure={})
])

gender = html.Div([

    html.H1("Average rating by gender and genre", style={'text-align': 'center'}),
    dcc.Graph(id='my_graph_gender', figure=createGenderPlot())
])

votes = html.Div([

    html.H1("Votes per rating", style={'text-align': 'center'}),
    dcc.Graph(id='my_graph_votes', figure=createVotesPlot())
])

gra1, gra2 = createActorsPlotOne()

actors = html.Div([

    html.H1("Composition of Stars", style={'text-align': 'center'}),
    html.Plaintext(
        "IMDB only returns a small number of main actors in an easily machine readable form.\nWe will consinder these as stars of the movie in the following charts."),
    dcc.Graph(id='my_graph_actors_one', figure=gra1),
    html.Br(),
    dcc.Graph(id='my_graph_actors_two', figure=gra2)
])

top = html.Div([
    html.H1("Top Movies", style={'text-align': 'center'}),
    html.Br(),
    html.Plaintext("The following movies are the top ten rated movies in the specified search criteria."),
    html.Plaintext(
        "The genre search down below is considered an \"or\" search and will not search for cumulated genres."),

    dcc.Dropdown(
        id="slct_genre_top",
        options=durationDrop(),
        multi=True,
        placeholder="Select a genre",
        value=[],
        clearable=True,
    ),
    html.Br(),
    dbc.Row([html.Plaintext("  Minimum number of votes:  "),
             dcc.Input(
                 id="min_votes_input_range", type="number", placeholder="input with range",
                 min=100, max=10000000, step=1, value=100, debounce=True
             )]),
    html.Div(id='output_container', children=[]),
    html.Br(),

    # no graph
    html.Div(id='my_graph_top', children=[])
])

"""Layout"""

app.layout = html.Div(
    [dcc.Location(id="url"), navbar, sidebar, content]
)

"""Callbacks"""


# Sidebar Callback
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Img(src='/assets/meme.jpg')  # Erklärung daten nur ab mind. 100 votes ab 1.1.2020
    elif pathname == "/page-1":
        return duration
    elif pathname == "/page-2":
        return gender
    elif pathname == "/page-3":
        return votes
    elif pathname == "/page-4":
        return top
    elif pathname == "/page-5":
        return actors
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


# Update Duration Graph
@app.callback(
    Output(component_id='my_graph', component_property='figure'),
    [Input(component_id='slct_genre', component_property='value')]
)
def update_graph(option_slcted):
    a = Analyse()
    dff = a.test_str(genres_list=option_slcted)
    dff2 = a.laenge(dff)

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, x_title="Duration in minutes",
                        subplot_titles=("Average rating by duration", "Number of movies"))
    fig.append_trace(
        go.Scatter(x=dff2.index, y=dff2['avg_vote_mean'], marker=Marker(dict(color="blue")), name="Average rating"),
        row=1, col=1)
    fig.append_trace(go.Scatter(x=dff2.index, y=dff2['avg_vote_25pct'], marker=Marker(dict(color="green", opacity=0.7)),
                                name="25pct"), row=1, col=1)
    fig.append_trace(
        go.Scatter(x=dff2.index, y=dff2['avg_vote_75pct'], marker=Marker(dict(color="red", opacity=0.7)), name="75pct"),
        row=1, col=1)
    fig.append_trace(go.Bar(x=dff2.index, y=dff2['title_counts'], name="Number of Movies"), row=2, col=1)
    return fig


@app.callback(
    Output(component_id='my_graph_top', component_property='children'),
    Input(component_id='slct_genre_top', component_property='value'),
    Input(component_id="min_votes_input_range", component_property='value')
)
def update_table_top(option_slcted, inpvote):
    b = Analyse()
    dff = b.test_str(genres_list=option_slcted)
    clean = dff[['imdb_title_id', 'title', 'avg_vote', 'votes']]
    clean_short = clean[clean['votes'] >= inpvote].sort_values('avg_vote', ascending=False).iloc[:10]
    if clean_short.empty:
        return dbc.Jumbotron(
            [
                html.H1("No Movies found with this arguments", className="text-danger"),
            ])
    else:
        return DashHelpers.topResult(clean_short)


if __name__ == "__main__":
    app.run_server(debug=True, port=8050, dev_tools_ui=False)
