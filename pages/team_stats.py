# pages/team_stats.py
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

def load_data():
    df = pd.read_csv("nba_games.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

def calculate_team_stats(df):
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
        html.Div([
            html.H1("NBA Team Rankings", className="mb-4 text-center"),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id='season-dropdown',
                        options=[{'label': f"{season}-{season+1}", 'value': season} for season in seasons],
                        value=seasons[0],
                        className="mb-4"
                    ),
                ], width=6),
            ], justify="center"),
            dbc.Spinner(
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='team-stats-chart')
                    ], width=12),
                ]),
                color="primary",
                type="border",
                fullscreen=True,
            )
        ], className="box-shadow container bg-white p-4 mb-4"),
        
        html.Div([
            html.H1("NBA Team Statistics", className="mb-4 text-center"),
            dbc.Row([
                dbc.Col([
                    dash_table.DataTable(
                        id='team-stats-table',
                        columns=[
                            {'name': 'Rank', 'id': 'rank'},
                            {'name': 'Team', 'id': 'team'},
                            {'name': 'Wins', 'id': 'wins'},
                            {'name': 'Losses', 'id': 'losses'},
                            {'name': 'Win %', 'id': 'win_percentage'},
                        ],
                        style_table={
                            'overflowX': 'auto',
                            'border': '1px solid #508D4E',
                            'border-radius': '8px'
                        },
                        style_cell={
                            'textAlign': 'center',
                            'padding': '10px',
                            'font-family': 'Arial, sans-serif',
                            'font-size': '14px',
                            'borderLeft': 'none',
                            'borderRight': 'none',
                            'borderTop': '1px solid #508D4E',
                            'borderBottom': '1px solid #508D4E',
                            'backgroundColor': '#e0f5ea'
                        },
                        style_header={
                            'backgroundColor': '#B6C6BE',
                            'fontWeight': 'bold',
                            'border': 'none'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#d1e4da'
                            },
                        ],
                        sort_action='native',
                        sort_mode='multi',
                        row_selectable='single'
                    ),
                ], width=12),
            ])
        ], className="box-shadow container bg-white p-4 mb-4"),
        html.Div(id='selected-team-stats')
    ])