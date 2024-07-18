# callbacks.py
from dash.dependencies import Input, Output
from pages.overall_stats import filter_data, get_player_stats
import urllib.parse

def register_callbacks(app):
    # Combined callback to update overall stats table and add hyperlinks
    @app.callback(
        Output('stats-table', 'data'),
        [Input('year-dropdown', 'value'),
         Input('season-type-dropdown', 'value')]
    )
    def update_table_with_links(selected_year, selected_season_type):
        filtered_data = filter_data(selected_year, selected_season_type)
        
        # Add hyperlinks to player names
        filtered_data['PLAYER'] = filtered_data['PLAYER'].apply(
            lambda x: f'<a href="/player/{urllib.parse.quote(x)}" target="_blank">{x}</a>'
        )
        
        return filtered_data.to_dict('records')

    # Callback to update player stats table based on player and season type
    @app.callback(
        [Output('player-stats-table', 'data'),
         Output('player-name-header', 'children')],
        [Input('url', 'pathname'),
         Input('player-season-type-dropdown', 'value')]
    )
    def update_player_stats(pathname, selected_season_type):
        if pathname.startswith('/player/'):
            player_name = urllib.parse.unquote(pathname.split('/')[-1])
            player_data = get_player_stats(player_name)
            filtered_data = player_data[player_data['Season_type'] == selected_season_type].drop(columns=['PLAYER', 'Season_type'])
            
            # Sort the data by Year in descending order
            filtered_data = filtered_data.sort_values('Year', ascending=False)
            
            return filtered_data.to_dict('records'), f"{player_name} Stats"
        return [], ""