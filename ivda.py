# Import necessary libraries
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Initialize the Dash app
app = Dash(__name__)

# Load the data from the CSV file
df = pd.read_csv('https://raw.githubusercontent.com/rezuanul/IVDA/main/df_fifa2.csv')

# Clean the data and prepare unique values for dropdowns
df = df[df['club_name'].notna() & df['nationality_name'].notna()]
unique_countries = df['nationality_name'].unique()
unique_clubs = df['club_name'].unique()
unique_positions = df['player_positions'].unique()
attributes = ['attacking', 'skill', 'movement', 'power', 'mentality', 'goalkeeping', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']

# Define the layout of the app
app.layout = html.Div([
    html.H2("Best Player Finder App", style={'text-align': 'center'}),
    # Dropdown for Gender Filter
    dcc.Dropdown(
        id='gender-filter',
        options=[
            {'label': 'All Genders', 'value': 'All'},
            {'label': 'Male', 'value': 'male'},
            {'label': 'Female', 'value': 'female'}
        ],
        value='All',
        style={'width': '48%', 'display': 'inline-block'}
    ),
    # Dropdown for Country Filter
    dcc.Dropdown(
        id='country-filter',
        options=[{'label': country, 'value': country} for country in unique_countries],
        value=unique_countries[0],
        style={'width': '48%', 'display': 'inline-block'}
    ),
    # Dropdown for Club Filter
    dcc.Dropdown(
        id='club-filter',
        options=[{'label': 'All Clubs', 'value': 'All'}] + [{'label': club, 'value': club} for club in unique_clubs if club is not None],
        value='All',
        style={'width': '48%', 'display': 'inline-block'}
    ),
    # Range Slider for Budget Filter
    html.Div(
        dcc.RangeSlider(
            id='budget-filter',
            min=df['value_eur'].min(),
            max=df['value_eur'].max(),
            step=100000,
            value=[df['value_eur'].min(), df['value_eur'].max()],
            marks={i: '{}'.format(i) for i in range(int(df['value_eur'].min()), int(df['value_eur'].max()), 10000000)}
        ),
        style={'width': '100%'}
    ),
    # Graph for Player Data Visualization
    dcc.Graph(id='player-data-graph'),

    # New section for top 10 players by attributes
    html.H2("Find Top 10 Players by Attributes and Positions", style={'text-align': 'center'}),
    dcc.Dropdown(
        id='attribute-filter',
        options=[{'label': attr, 'value': attr} for attr in attributes],
        value='attacking',
        style={'width': '48%', 'display': 'inline-block'}
    ),
    dcc.Dropdown(
        id='position-filter',
        options=[{'label': pos, 'value': pos} for pos in unique_positions],
        value='All',
        style={'width': '48%', 'display': 'inline-block'}
    ),
    dcc.Graph(id='top-players-bar-chart'),
    dcc.Graph(id='players-clustering-graph'),
])

# Callback for updating the player scatter plot
@app.callback(
    Output('player-data-graph', 'figure'),
    [Input('gender-filter', 'value'),
     Input('country-filter', 'value'),
     Input('club-filter', 'value'),
     Input('budget-filter', 'value')]
)
def update_player_scatter_plot(gender_value, country_value, club_value, budget_range):
    filtered_df = df.copy()
    if gender_value != 'All':
        filtered_df = filtered_df[filtered_df['gender'] == gender_value]
    if club_value != 'All':
        filtered_df = filtered_df[filtered_df['club_name'] == club_value]

    filtered_df = filtered_df[
        (filtered_df['nationality_name'] == country_value) &
        (filtered_df['value_eur'] >= budget_range[0]) &
        (filtered_df['value_eur'] <= budget_range[1])
    ]

    fig = px.scatter(filtered_df, x="age", y="overall", color="nationality_name",
                     size="value_eur", hover_data=["short_name", "club_name", "nationality_name"])
    return fig

# Callback for updating the top 10 players bar chart
@app.callback(
    Output('top-players-bar-chart', 'figure'),
    [Input('attribute-filter', 'value'),
     Input('position-filter', 'value')]
)
def update_top_players_chart(attribute, position):
    filtered_df = df.copy()
    if position != 'All':
        filtered_df = filtered_df[filtered_df['player_positions'].str.contains(position)]
    top_players = filtered_df.nlargest(10, attribute)
    fig = px.bar(top_players, x='short_name', y=attribute, color=attribute)
    return fig

# Callback for clustering players based on the selected attribute
@app.callback(
    Output('players-clustering-graph', 'figure'),
    [Input('attribute-filter', 'value')]
)
def cluster_players(attribute):
    # Simple KMeans clustering
    kmeans = KMeans(n_clusters=3)
    # Normalize the attribute for clustering
    scaler = StandardScaler()
    df['normalized_attr'] = scaler.fit_transform(df[[attribute]])
    df['cluster'] = kmeans.fit_predict(df[['normalized_attr']])
    fig = px.scatter(df, x='age', y='overall', color='cluster', hover_data=['short_name'])
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)