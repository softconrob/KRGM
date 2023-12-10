# Import necessary libraries
import dash
from dash import Dash, dcc, html, Input, Output, dash_table, State
from dash.dependencies import ALL
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import euclidean

# Initialize the Dash app
app = Dash(__name__)

# Load and clean the data
df = pd.read_csv('https://raw.githubusercontent.com/softconrob/KRGM/main/df_fifa4.csv')
df = df[df['club_name'].notna() & df['nationality_name'].notna()]

# Prepare unique values for dropdowns and other controls
unique_countries = ['All Countries'] + list(df['nationality_name'].unique())
unique_clubs = ['All Clubs'] + list(df['club_name'].unique())
unique_positions = df['player_positions'].unique()
attributes = ['attacking', 'skill', 'movement', 'power', 'mentality', 'goalkeeping', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
player_names = df['short_name'].unique()

# Adding a column for country counts
country_counts = df['nationality_name'].value_counts().reset_index()
country_counts.columns = ['country', 'player_count']

# Define the layout of the app
app.layout = html.Div([
    html.Div([
    # Filters for gender, country, club, and budget
        html.H2("FIFA Player Mixed Gender Finder App", style={'text-align': 'center'}),
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
    dcc.Dropdown(
        id='country-filter',
        options=[{'label': country, 'value': country} for country in unique_countries],
        value='All Countries',
        style={'width': '48%', 'display': 'inline-block'}
    ),
    dcc.Dropdown(
        id='club-filter',
        options=[{'label': club, 'value': club} for club in unique_clubs],
        value='All Clubs',
        style={'width': '48%', 'display': 'inline-block'}
    ),
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

    # Scatter plot for player data visualization
    dcc.Graph(id='player-data-graph'),

    # World map for displaying players by country
    dcc.Graph(id='world-map-players'),

    # Section for top 10 players by attributes
    html.H2("Find Top 10 Players by Attributes and Position", style={'text-align': 'center'}),
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
    dcc.ConfirmDialog(
        id='confirm-dialog',
        message='Do you want to add this player to the team?',
    ),

    # Section for clustering players based on the selected attribute
    html.H2("Clustering Players based on Player Attributes and Age", style={'text-align': 'center'}),
    dcc.Graph(id='players-clustering-graph'),

    # Section for finding similar players
    html.H2("Find Similar Players", style={'text-align': 'center'}),
    dcc.Dropdown(
        id='player-search',
        options=[{'label': name, 'value': name} for name in player_names],
        value=player_names[0],
        style={'width': '48%', 'display': 'inline-block'}
    ),
    html.Div(id='similar-players-details'),
    dcc.Graph(id='similar-players-attributes-chart'),

    # New section for player comparison
    html.H2("Compare Players", style={'text-align': 'center'}),
    dcc.Dropdown(
        id='player-comparison-selection',
        options=[{'label': name, 'value': name} for name in player_names],
        value=[player_names[0], player_names[1]],
        multi=True,
        style={'width': '60%', 'margin': '10px auto'}
    ),
    html.Div(id='player-comparison-details'),
    dcc.Graph(id='player-comparison-bar-chart'),
], id='main-container', style={'width': '95%', 'margin': '0 auto'})
])

side_panel = html.Div([
    html.H2("Team", style={'text-align': 'center'}),
    dcc.Dropdown(
        id='player-dropdown',
        options=[{'label': player, 'value': player} for player in player_names],
        placeholder='Select a player',
        style={'width': '100%', 'margin-bottom': '10px'},
    ),
    html.Button('Add to Team', id='add-to-cart-button', n_clicks=0, style={'width': '100%'}),
    dcc.Store(id='player-list', data=[]),
    html.Ul(id='player-cart-list', style={'list-style-type': 'none', 'margin-top': '10px'}),
    html.Div(id='total-budget', style={'margin-top': '10px'}),
    html.Div(id='total-rating', style={'margin-top': '10px'}),
], id='side-panel', style={'position': 'fixed', 'top': 0, 'right': '-300px', 'width': '300px', 'height': '100%', 'background-color': '#f8f9fa', 'padding': '20px', 'transition': '0.5s'})

# Add the side panel to the layout
app.layout.children.append(side_panel)

# Callback for updating the player scatter plot and world map
@app.callback(
    [Output('player-data-graph', 'figure'), Output('world-map-players', 'figure')],
    [Input('gender-filter', 'value'),
     Input('country-filter', 'value'),
     Input('club-filter', 'value'),
     Input('budget-filter', 'value')]
)
def update_visualizations(gender_value, country_value, club_value, budget_range):
    # Filter the DataFrame based on the selection
    filtered_df = df.copy()
    if gender_value != 'All':
        filtered_df = filtered_df[filtered_df['gender'] == gender_value]
    if country_value != 'All Countries':
        filtered_df = filtered_df[filtered_df['nationality_name'] == country_value]
    if club_value != 'All Clubs':
        filtered_df = filtered_df[filtered_df['club_name'] == club_value]

    filtered_df = filtered_df[
        (filtered_df['value_eur'] >= budget_range[0]) &
        (filtered_df['value_eur'] <= budget_range[1])
    ]

    # Create the scatter plot
    scatter_fig = px.scatter(filtered_df, x="age", y="overall", color="nationality_name",
                             size="value_eur", hover_data=["short_name", "club_name", "nationality_name"])

    # Adjusting the world map based on the selection
    map_df = df if country_value == 'All Countries' else filtered_df
    country_map_counts = map_df['nationality_name'].value_counts().reset_index()
    country_map_counts.columns = ['country', 'player_count']

    world_map_fig = go.Figure(data=go.Choropleth(
        locations=country_map_counts['country'],
        z=country_map_counts['player_count'],
        locationmode='country names',
        colorscale='Viridis',
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title='Number of Players',
    ))
    world_map_fig.update_layout(title_text='Player Distribution by Country', geo=dict(showframe=False))

    return scatter_fig, world_map_fig

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
    kmeans = KMeans(n_clusters=3)
    scaler = StandardScaler()
    df['normalized_attr'] = scaler.fit_transform(df[[attribute]])
    df['cluster'] = kmeans.fit_predict(df[['normalized_attr']])
    fig = px.scatter(df, x='age', y='overall', color='cluster', hover_data=['short_name'])
    return fig

# Callback for updating the similar players section with photos and attributes
@app.callback(
    [Output('similar-players-details', 'children'),
     Output('similar-players-attributes-chart', 'figure')],
    [Input('player-search', 'value')]
)
def update_similar_players(selected_player_name):
    selected_player = df[df['short_name'] == selected_player_name].iloc[0]
    df['similarity'] = df.apply(lambda row: euclidean(row[attributes + ['overall']], selected_player[attributes + ['overall']]), axis=1)
    similar_players = df.nsmallest(6, 'similarity')

    # Create a div for player photos and names
    player_photos_and_names = html.Div([
        html.Div([
            html.Img(src=player['player_face_url'], style={'height': '100px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}),
            html.P(player['short_name'], style={'text-align': 'center'})
        ], style={'display': 'inline-block', 'margin': '10px'}) for _, player in similar_players.iterrows()
    ], style={'textAlign': 'center'})

    # Melt the DataFrame for line chart visualization
    melted_df = pd.melt(similar_players, id_vars=['short_name'], value_vars=attributes + ['overall'], var_name='Attribute', value_name='Value')
    attributes_chart = px.line(melted_df, x='Attribute', y='Value', color='short_name', markers=True, title='Attributes of Similar Players')

    return player_photos_and_names, attributes_chart

# Callback for updating the player comparison section with table and bar chart
@app.callback(
    [Output('player-comparison-details', 'children'),
     Output('player-comparison-bar-chart', 'figure')],
    [Input('player-comparison-selection', 'value')]
)
def update_player_comparison(selected_players):
    if selected_players:
        comparison_df = df[df['short_name'].isin(selected_players)]

        # Create a layout for player photos and names
        player_info = html.Div([
            html.Div([
                html.Img(src=player['player_face_url'], style={'height': '100px'}),
                html.H5(player['short_name'])
            ], style={'display': 'inline-block', 'margin': '10px'}) for _, player in comparison_df.iterrows()
        ], style={'textAlign': 'center'})

        # Melt the DataFrame for line chart visualization
        comparison_attributes = ['overall', 'age'] + attributes
        melted_comparison_df = pd.melt(comparison_df, id_vars=['short_name'], value_vars=comparison_attributes, var_name='Attribute', value_name='Value')
        line_chart_fig = px.line(melted_comparison_df, x='Attribute', y='Value', color='short_name', markers=True, title='Player Attribute Comparison')

        return player_info, line_chart_fig
    else:
        return html.Div("Please select players to compare."), {}

# Callback for showing the side panel on hover
@app.callback(
    Output('side-panel', 'style'),
    [Input('main-container', 'n_clicks'),
     Input('side-panel', 'n_clicks')],
    prevent_initial_call=True
)
def toggle_side_panel(main_click, side_click):
    ctx = dash.callback_context

    if ctx.triggered_id == 'main-container':
        # Click on the main container, keep it closed
        return {'position': 'fixed', 'top': 0, 'right': '-300px', 'width': '300px', 'height': '100%', 'background-color': '#f8f9fa', 'padding': '20px', 'transition': '0.5s'}
    elif ctx.triggered_id == 'side-panel':
        # Click on the side panel, keep it open
        return {'position': 'fixed', 'top': 0, 'right': '0', 'width': '300px', 'height': '100%', 'background-color': '#f8f9fa', 'padding': '20px', 'transition': '0.5s'}
    else:
        # No valid trigger, return the current style
        return dash.no_update

@app.callback(
    [Output('player-list', 'data'),
     Output('player-cart-list', 'children'),
     Output('total-budget', 'children'),
     Output('total-rating', 'children')],
    [Input('add-to-cart-button', 'n_clicks'),
     Input({'type': 'remove-player-button', 'index': ALL}, 'n_clicks'),
     Input('confirm-dialog', 'submit_n_clicks')],
    [State('player-dropdown', 'value'),
     State('player-list', 'data'),
     State('top-players-bar-chart', 'clickData')],
    prevent_initial_call=True
)
def update_player_list(add_clicks, remove_clicks, submit_n_clicks, player, player_list, click_data):
    ctx = dash.callback_context
    triggered_id = ctx.triggered_id if ctx.triggered_id else 'add-to-cart-button'

    if triggered_id == 'confirm-dialog':
        player_name = click_data['points'][0]['x']
        if player_name not in player_list:
            player_list.append(player_name)
    elif triggered_id == 'add-to-cart-button' and player is not None and player not in player_list:
        # Add player
        player_list.append(player)
    # is triggered_id can get 'type'
    elif triggered_id.get('type').startswith('remove-player-button'):
        # Remove player based on the index in the triggered ID
        indices_to_remove = [int(triggered_id['index']) for remove_click in remove_clicks]
        indices_to_remove = [index for index in indices_to_remove if 0 <= index < len(player_list)]
        player_list = [player for i, player in enumerate(player_list) if i not in indices_to_remove]

    # update totoal budget and team rating
    total_budget = 0
    total_rating = 0
    player_positions = []
    player_faces = []
    for player in player_list:
        total_budget += df[df['short_name'] == player]['value_eur'].values[0]
        total_rating += df[df['short_name'] == player]['overall'].values[0]
        player_positions.append(df[df['short_name'] == player]['player_positions'].values[0])
        player_faces.append(df[df['short_name'] == player]['player_face_url'].values[0])
    average_rating = total_rating / len(player_list)
    # format the total budget to millions
    total_budget = total_budget / 1000000
    
    total_budget = 'Total value: ' + str(total_budget) + 'M €' 
    total_rating = 'Team Rating: ' + str(average_rating)

    # Prepare updated player cart children
    player_cart_children = [
    html.Div(
        [
            html.Div(player_positions[i], className="position"),
            html.Img(
                src=player_faces[i],
                style={'width': '50px', 'height': '50px', 'margin-right': '10px'}
            ),
            html.P(player, className="player-name"),
            html.Button(
                'Remove',
                id={'type': 'remove-player-button', 'index': i},
                n_clicks=0,
                className="remove-button"
            ),
        ], className="player-cart-item", style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}
    )
    for i, player in enumerate(player_list)
]

    return player_list, player_cart_children, total_budget, total_rating

# callback for detecting changes in the bar chart, it should show a pop-up window about whether the user wants to add the player to the team
@app.callback(
    Output('confirm-dialog', 'displayed'),
    [Input('top-players-bar-chart', 'clickData')],
    prevent_initial_call=True
)
def show_popup(click_data):
    if click_data is not None:
        return True
    else:
        return False
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)