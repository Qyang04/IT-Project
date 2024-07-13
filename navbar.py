# navbar.py
from dash import html, dcc

def create_navbar():
    return html.Nav([
        html.Div([
            html.A("NBA Prediction Dashboard", href="/", className="navbar-brand"),
            html.Ul([
                html.Li(dcc.Link("Home", href="/")),
                html.Li(dcc.Link("Player Stats", href="/player-stats")),
                # Add more navigation items here as needed
            ], className="navbar-nav")
        ], className="container")
    ], className="navbar")