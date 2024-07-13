import dash
from dash import html, dcc
from dash.dependencies import Input, Output

from layouts import main_layout, player_stats_layout
import callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/player-stats':
        return player_stats_layout()
    else:
        return main_layout()

if __name__ == '__main__':
    app.run_server(debug=True)