# callbacks.py
from dash.dependencies import Input, Output
from pages.overall_stats import filter_data, get_player_stats
import urllib.parse
import pandas as pd
import plotly.express as px
import pickle

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
    
    # callback for team stats
    @app.callback(
        [Output('team-stats-table', 'data'),
         Output('team-stats-chart', 'figure')],
        [Input('season-dropdown', 'value')]
    )
    def update_team_stats(selected_season):
        # Load and preprocess data
        df = pd.read_csv("nba_games.csv")
        df['date'] = pd.to_datetime(df['date'])
        
        # Calculate season based on the date
        df['season'] = df['date'].apply(lambda x: x.year if x.month >= 10 else x.year - 1)
        
        # Filter data for the selected season
        season_data = df[df['season'] == selected_season]
        
        # Calculate team stats
        team_stats = season_data.groupby('team').agg({
            'won': ['sum', 'count']
        }).reset_index()
        team_stats.columns = ['team', 'wins', 'games_played']
        team_stats['losses'] = team_stats['games_played'] - team_stats['wins']
        team_stats['win_percentage'] = team_stats['wins'] / team_stats['games_played']
        
        # Sort teams by win percentage and assign ranks
        team_stats = team_stats.sort_values('win_percentage', ascending=False).reset_index(drop=True)
        team_stats['rank'] = team_stats.index + 1
        
        # Prepare data for the table
        table_data = team_stats[['rank', 'team', 'wins', 'losses', 'win_percentage']].to_dict('records')
        for record in table_data:
            record['win_percentage'] = f"{record['win_percentage']:.3f}"
        
        # Create bar chart
        fig = px.bar(
            team_stats,
            x='team',
            y='win_percentage',
            title=f'Team Win Percentages for {selected_season}-{selected_season+1} Season',
            labels={'team': 'Team', 'win_percentage': 'Win Percentage'},
            color='win_percentage',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(xaxis={'categoryorder': 'total descending'})
        
        return table_data, fig