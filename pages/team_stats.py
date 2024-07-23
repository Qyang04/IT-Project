# pages/team_stats.py
from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px

def load_data():
    # Read directly from the CSV file
    df = pd.read_csv("nba_games.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

def calculate_team_stats(df):
    # Calculate season based on the date
    df['season'] = df['date'].apply(lambda x: x.year if x.month >= 10 else x.year - 1)
    
    team_stats = df.groupby(['season', 'team']).agg({
        'won': ['sum', 'count']
    }).reset_index()
    team_stats.columns = ['season', 'team', 'wins', 'games_played']
    team_stats['losses'] = team_stats['games_played'] - team_stats['wins']
    team_stats['win_percentage'] = team_stats['wins'] / team_stats['games_played']
    return team_stats

def team_stats_content():
    df = load_data()
    team_stats = calculate_team_stats(df)
    
    seasons = sorted(team_stats['season'].unique(), reverse=True)
    
    return html.Div([
        html.H1("Team Stats and Rankings", className="mb-4"),
        html.Div([
            dcc.Dropdown(
                id='season-dropdown',
                options=[{'label': f"{season}-{season+1}", 'value': season} for season in seasons],
                value=seasons[0],
                className="mb-4"
            ),
            dash_table.DataTable(
                id='team-stats-table',
                columns=[
                    {'name': 'Rank', 'id': 'rank'},
                    {'name': 'Team', 'id': 'team'},
                    {'name': 'Wins', 'id': 'wins'},
                    {'name': 'Losses', 'id': 'losses'},
                    {'name': 'Win Percentage', 'id': 'win_percentage'},
                ],
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'font-family': 'Arial, sans-serif',
                    'font-size': '14px'
                },
                style_header={
                    'backgroundColor': '#f2f2f2',
                    'fontWeight': 'bold',
                    'border': 'none'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f9f9f9'
                    },
                ],
                sort_action='native',
                sort_mode='multi',
            ),
            dcc.Graph(id='team-stats-chart')
        ], className="box-shadow container bg-white rounded p-4 mb-4")
    ])