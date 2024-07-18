# layouts.py
from dash import html
from pages.main_page import main_page_content
from pages.overall_stats import overall_stats_content
from pages.individual_player_stats import individual_player_stats_content
from sidebar import create_sidebar

def create_layout(content):
    return html.Div([
        html.Link(
            rel='stylesheet',
            href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'
        ),
        html.Link(
            rel='stylesheet',
            href='https://fonts.googleapis.com/icon?family=Material+Icons'
        ),
        create_sidebar(),
        html.Div([
            html.Div([
                content
            ], className="container")
        ], id="main-content")
    ])

def main_layout():
    return create_layout(main_page_content())

def overall_stats_layout():
    return create_layout(overall_stats_content())

def individual_player_stats_layout():
    return create_layout(individual_player_stats_content())