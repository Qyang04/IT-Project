# pages/overall_stats.py
from dash import dcc, html, dash_table
import pandas as pd

# Load data
data = pd.read_csv("nba_player_stats.csv")

# Remove PLAYER_ID and TEAM_ID columns
data = data.drop(columns=['PLAYER_ID', 'TEAM_ID'])

# Rename "Regular%20Season" to "Regular Season"
data['Season_type'] = data['Season_type'].replace('Regular%20Season', 'Regular Season')

# Extract unique years, season types, and players
years = data['Year'].unique()
season_types = data['Season_type'].unique()

def overall_stats_content():
    return html.Div([
        html.Div([
            html.H1("NBA Player Stats Dashboard", className="mb-4 text-center"),
        
            html.Div([
                html.Div([
                    html.Label("Select Year:"),
                    dcc.Dropdown(
                        id='year-dropdown',
                        options=[{'label': str(year), 'value': year} for year in years],
                        value=years[0],
                        style={'width': '200px'}
                    ),
                ], className="me-3"),
                
                html.Div([
                    html.Label("Select Season Type:"),
                    dcc.Dropdown(
                        id='season-type-dropdown',
                        options=[{'label': season_type, 'value': season_type} for season_type in season_types],
                        value=season_types[0],
                        style={'width': '200px'}
                    ),
                ]),
            ], className="d-flex justify-content-end mb-4"),
            
            dash_table.DataTable(
                id='stats-table',
                columns=[
                    {"name": i, "id": i, "presentation": "markdown"} if i == "PLAYER" else {"name": i, "id": i}
                    for i in data.columns if i not in ['Year', 'Season_type']
                ],
                page_size=20,
                style_table={'overflowX': 'auto'},
                style_cell_conditional=[
                    {'if': {'column_id': 'PLAYER'},
                    'textAlign': 'left'},
                    {'if': {'column_id': 'Year'},
                    'display': 'none'},
                    {'if': {'column_id': 'Season_type'},
                    'display': 'none'}
                ],
                style_header={
                    'fontWeight': 'bold'
                },
                style_cell={
                    'textAlign': 'center',
                    'padding': '5px'
                },
                markdown_options={"html": True}  # Allow HTML in markdown
            )
        ], className="box-shadow container bg-white p-4 mb-4")
    ])

# Define filter_data and get_player_stats functions
def filter_data(year, season_type):
    filtered_data = data[(data['Year'] == year) & (data['Season_type'] == season_type)]
    return filtered_data.drop(columns=['Year', 'Season_type'])

def get_player_stats(player_name):
    player_data = data[data['PLAYER'] == player_name]
    return player_data
