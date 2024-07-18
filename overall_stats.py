import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
from dash.exceptions import PreventUpdate
import urllib.parse

# Load data
data = pd.read_csv("nba_player_stats.csv")

# (Keep the rest of the data processing code)

# Define layouts and callback functions
overall_stats_layout = html.Div([
    # (Keep the layout definition)
])

player_stats_layout = html.Div([
    # (Keep the layout definition)
])

# Define filter_data and get_player_stats functions

# Define callback functions
def update_table_with_links(selected_year, selected_season_type):
    # (Keep the function implementation)

def update_player_stats(pathname, selected_season_type):
    # (Keep the function implementation)