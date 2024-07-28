# pages/individual_player_stats.py
from dash import html, dcc, dash_table
from pages.overall_stats import season_types, data

def get_player_image_url(player_name):
    # convert player name to the format used in Basketball-Reference URLs
    formatted_name = player_name.lower().replace(" ", "_")
    # extract the first 5 letters of the last name and the first 2 of the first name
    last_name = formatted_name.split("_")[-1][:5]
    first_name = formatted_name.split("_")[0][:2]
    return f"https://www.basketball-reference.com/req/202106291/images/headshots/{last_name}{first_name}01.jpg"

def get_player_career_stats(player_name, season_type):
    player_data = data[(data['PLAYER'] == player_name) & (data['Season_type'] == season_type)]
    
    if player_data.empty:
        return None
    
    career_stats = {
        'Seasons Played': player_data['Year'].nunique(),
        'Total Games Played': f"{player_data['GP'].sum()}",
        'Highest Overall Rank': f"{player_data['RANK'].min()} ({player_data.loc[player_data['RANK'].idxmin(), 'Year']})",
        'Best PPG Season': f"{player_data['PTS'].max():.1f} ({player_data.loc[player_data['PTS'].idxmax(), 'Year']})",
        'Best APG Season': f"{player_data['AST'].max():.1f} ({player_data.loc[player_data['AST'].idxmax(), 'Year']})",
        'Best RPG Season': f"{player_data['REB'].max():.1f} ({player_data.loc[player_data['REB'].idxmax(), 'Year']})"
    }
    
    return career_stats

def individual_player_stats_content():
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    # player image
                    html.Div([
                        html.H1(id='player-name-header', className="mb-4"),
                        html.Img(id='player-image', style={'max-width': '250px', 'max-height': '250px'}),
                    ], className="col-5 text-center"),
                    
                    # dropdown
                    html.Div([
                        html.Label("Select Season Type:", className="mt-4"),
                        dcc.Dropdown(
                            id='player-season-type-dropdown',
                            options=[{'label': season_type, 'value': season_type} for season_type in season_types],
                            value=season_types[0],
                            style={'width': '250px'}
                        ),
                        # career stats
                        html.Div(id='player-career-stats', className="my-4")
                    ], className="col-7")
                ], className="row justify-content-center align-items-center")
            ], className="align-middle"),
        ], className="box-shadow container bg-white rounded p-4 mb-4"),
        
        
        # player data
        html.Div([
            html.H1("Player Statistics", className="mb-4 text-center"),
            dash_table.DataTable(
                id='player-stats-table',
                columns=[{"name": i, "id": i} for i in data.columns if i not in ['PLAYER', 'Season_type']],
                style_table={'overflowX': 'auto', 'padding-left': '1px'},
                style_cell_conditional=[
                    {'if': {'column_id': 'Year'},
                    'textAlign': 'left'},
                ],
                style_cell={
                    'textAlign': 'center',
                    'padding': '5px',
                    'border': '1px solid #508D4E'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#D6EFD8'
                    }
                ],
                style_header={
                    'fontWeight': 'bold',
                    'background': '#B5CFB7'
                },
            )
        ], className="box-shadow container bg-white rounded p-4 mb-4")
    ])