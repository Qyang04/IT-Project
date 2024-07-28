# callbacks.py
from bs4 import BeautifulSoup
from dash.dependencies import Input, Output, State
import requests
from pages.individual_player_stats import get_player_career_stats, get_player_image_url
from pages.overall_stats import filter_data, get_player_stats
import urllib.parse
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash import html, dcc
import xml.etree.ElementTree as ET


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
         Output('player-name-header', 'children'),
         Output('player-image', 'src'),
         Output('player-career-stats', 'children')],
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
            
            # Get the player image URL
            player_image_url = get_player_image_url(player_name)
            
            # Get career stats
            career_stats = get_player_career_stats(player_name, selected_season_type)
        
            # Create a layout for career stats
            if career_stats:
                career_stats_layout = html.Div([
                    html.H3(f"Career Highlights ({selected_season_type})", className="mb-4"),
                    html.Div([
                        html.Div([
                            html.P([
                                html.Strong(f"{key}: "),
                                f"{value:}"
                            ])
                            for key, value in list(career_stats.items())[i:i+3]
                        ], className="col-lg-6")
                    for i in range(0, len(career_stats), 3)
                    ], className="row")
                ])
            
            return filtered_data.to_dict('records'), f"{player_name} Stats", player_image_url, career_stats_layout
        return [], "", "", html.Div()
    
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
            y='team',
            x='win_percentage',
            title=f'Team Win Percentages for {selected_season}-{selected_season+1} Season',
            labels={'team': 'Team', 'win_percentage': 'Win Percentage'},
            color='win_percentage',
            color_continuous_scale='rdylgn',
            orientation='h'
        )
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title="Win Percentage", 
            yaxis_title="Team",
            height=1000,
            margin=dict(l=150),
            bargap=0.2
        )
        fig.update_traces(
            texttemplate='%{x:.1%}', 
            textposition='outside', # add % at the end of bar
        ) 
        
        return table_data, fig
    
    @app.callback(
        Output('selected-team-stats', 'children'),
        [Input('team-stats-table', 'selected_rows'),
         Input('team-stats-table', 'data'),
         Input('season-dropdown', 'value')]
    )
    def display_selected_team_stats(selected_rows, table_data, selected_season):
        if not selected_rows:
            return html.Div()
        
        selected_team = table_data[selected_rows[0]]['team']
        
        df = pd.read_csv("nba_games.csv")
        df['date'] = pd.to_datetime(df['date'])
        df['season'] = df['date'].apply(lambda x: x.year if x.month >= 10 else x.year - 1)
        
        team_data = df[(df['team'] == selected_team) & (df['season'] == selected_season)]
        
        cumulative_wins = team_data['won'].cumsum()
        cumulative_losses = (~team_data['won'].astype(bool)).cumsum()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=team_data['date'].astype(str), y=cumulative_wins, mode='lines', name='Wins'))
        fig.add_trace(go.Scatter(x=team_data['date'].astype(str), y=cumulative_losses, mode='lines', name='Losses'))
        fig.update_layout(title=f"{selected_team} Win-Loss Record for {selected_season}-{selected_season+1} Season",
                          xaxis_title="Date", yaxis_title="Games", xaxis=dict(tickformat='%Y-%m-%d', tickmode='auto', nticks=10))
        
        return html.Div([
            html.H1(f"Detailed Stats for {selected_team}", className="mb-4 text-center"),
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.P([
                            html.Strong("Total Games: "), 
                            f"{len(team_data)}"
                        ]),
                        html.P([
                            html.Strong("Home Games: "), 
                            f"{len(team_data[team_data['home'] == 1])}"
                        ]),
                        html.P([
                            html.Strong("Away Games: "), 
                            f"{len(team_data[team_data['home'] == 0])}"
                        ]),
                        html.P([
                            html.Strong("Points Scored: "), 
                            f"{team_data['pts'].sum()}"
                        ]),
                        html.P([
                            html.Strong("Points Allowed: "), 
                            f"{team_data['pts_opp'].sum()}"
                        ]),
                    ], width=3),
                    dbc.Col([
                        dcc.Graph(figure=fig)
                    ], width=8)
                ], align="center", justify="center")
            ], className="align-middle")
        ], className="box-shadow container bg-white p-4 my-4")
        
    @app.callback(
        Output('nba-news-feed', 'children'),
        Input('url', 'pathname')
    )
    def update_news_feed(pathname):
        if pathname == '/fan-zone':
            try:
                url = "https://www.sportingnews.com/au/nba/news"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                news_items = soup.find_all('div', class_='md:flex md:flex-col group')[:5]
                
                if not news_items:
                    return html.Div("No news items found. The website structure might have changed.")
                
                news_list = []
                for item in news_items:
                    link_elem = item.find('a', role='article')
                    title_elem = item.find('h3', class_='font-bold')
                    img_elem = item.find('img', class_='object-cover')
                    
                    if link_elem and title_elem and img_elem:
                        title = title_elem.text.strip()
                        link = link_elem['href']
                        img_src = img_elem['src']
                        author_elem = item.find('p', class_='p-0 m-0 font-medium leading-9.38px uppercase text-d4 whitespace-nowrap text-8px md:text-10px h-2 md:h-2.5')
                        author = author_elem.text if author_elem else "Unknown"
                        time_elem = item.find('time')
                        time = time_elem['datetime'] if time_elem else "Unknown"
                        
                        news_item = html.Li([
                            html.Div([
                                html.Img(src=img_src, className="news-image"),
                                html.Div([
                                    html.A(title, href=link, target="_blank", className="news-title"),
                                    html.Div([
                                        html.Span(f"By {author}", className="news-author"),
                                        html.Span(" • ", className="news-separator"),
                                        html.Span(time, className="news-time")
                                    ], className="news-metadata")
                                ], className="news-content")
                            ], className="news-item-container")
                        ])
                        news_list.append(news_item)
                    else:
                        news_list.append(html.Li("Error parsing news item"))
                
                return html.Ul(news_list, className="news-list") if news_list else html.Div("No valid news items found")
            
            except requests.RequestException as e:
                return html.Div(f"Error fetching news: {str(e)}")
            except Exception as e:
                return html.Div(f"An unexpected error occurred: {str(e)}")
        
        return html.Div("News feed is only available on the Fan Zone page")
