# # layouts.py
# from dash import html
# from pages.main_page import main_page_content
# from pages.player_stats import player_stats_content
# from navbar import create_navbar


# def main_layout():
#     return html.Div([
#         html.Link(
#             rel='stylesheet',
#             href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'
#         ),
#         create_navbar(),
#         html.Div([
#             html.Div([
#                 main_page_content()
#             ], className="container")
#         ], style={'backgroundColor': '#f0f0f0', 'minHeight': 'calc(100vh - 56px)', 'padding': '20px'})
#     ])

# def player_stats_layout():
#     return html.Div([
#         create_navbar(),
#         html.Div([
#             html.Div([
#                 player_stats_content()
#             ], className="container")
#         ], style={'backgroundColor': '#f0f0f0', 'minHeight': 'calc(100vh - 56px)', 'padding': '20px'})
#     ])

# layouts.py
from dash import html
from pages.main_page import main_page_content
from pages.player_stats import player_stats_content
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

def player_stats_layout():
    return create_layout(player_stats_content())