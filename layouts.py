# layouts.py
from dash import html
from pages.main_page import main_page_content
from pages.player_stats import player_stats_content
from navbar import create_navbar

def main_layout():
    return html.Div([
        create_navbar(),
        html.Div([
            html.Div([
                main_page_content()
            ], className="container")
        ], style={'backgroundColor': '#f0f0f0', 'minHeight': 'calc(100vh - 56px)', 'padding': '20px 0px 0px 0px'})
    ])

def player_stats_layout():
    return html.Div([
        create_navbar(),
        html.Div([
            html.Div([
                player_stats_content()
            ], className="container")
        ], style={'backgroundColor': '#f0f0f0', 'minHeight': 'calc(100vh - 56px)', 'padding': '20px'})
    ])