# pages/individual_player_stats.py
from dash import html, dcc, dash_table
from pages.overall_stats import season_types, data

def individual_player_stats_content():
    return html.Div([
        html.Div([
            html.H1(id='player-name-header'),
            html.Div([
                html.Label("Select Season Type:"),
                dcc.Dropdown(
                    id='player-season-type-dropdown',
                    options=[{'label': season_type, 'value': season_type} for season_type in season_types],
                    value=season_types[0],
                    style={'width': '150px'}
                ),
            ]),
            dash_table.DataTable(
                id='player-stats-table',
                columns=[{"name": i, "id": i} for i in data.columns if i not in ['PLAYER', 'Season_type']],
                style_table={'overflowX': 'auto'},
                style_cell_conditional=[
                    {'if': {'column_id': 'Year'},
                    'textAlign': 'left'},
                ],
                style_cell={
                    'textAlign': 'center',
                    'padding': '5px'
                }
            )
        ], className="box-shadow container bg-white rounded p-4 mb-4")
    ])