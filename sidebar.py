# sidebar.py
from dash import html, dcc

def create_sidebar():
    return html.Div([
        # html.Button("☰", id="sidebar-toggle", className="sidebar-toggle"),
        html.Div([
            dcc.Link([
                html.I(className="material-icons", children="home"),
                html.Span("Home", className="icon-text")
            ], href="/", className="sidebar-link"),
            dcc.Link([
                html.I(className="material-icons", children="person"),
                html.Span("Player Stats", className="icon-text")
            ], href="/player-stats", className="sidebar-link"),
            # Add more navigation items here as needed
        ], id="sidebar-content")
    ], id="sidebar")