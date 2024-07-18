# app.py
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import urllib.parse

from layouts import main_layout, overall_stats_layout, individual_player_stats_layout
import callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/overall-stats':
        return overall_stats_layout()
    elif pathname.startswith('/player/'):
        return individual_player_stats_layout()
    elif pathname == '/':
        return main_layout()
    else:
        return '404 Page Not Found'

# Register callbacks
callbacks.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)