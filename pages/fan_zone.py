# pages/fan_zone.py
from dash import html, dcc

def fan_zone_content():
    return html.Div([
        html.H1("NBA Fan Zone", className="mb-4 text-center"),
        
        # Video Highlights Section
        html.Div([
            html.H2("NBA Highlights", className="mb-3"),
            
            # Channel Section
            html.Div([
                html.Img(src="/assets/nbapic.jpg", className="border-circle", style={"max-width": "150px"}),
                html.H3("NBA YouTube Channel", className="mt-2"),
                html.P("Welcome! Click on the button below to watch more amazing highlights of NBA Players!"),
                html.A("Visit Channel", href="https://www.youtube.com/nba", target="_blank", 
                       className="btn btn-primary mt-2")
            ], className="text-center mb-5"),
            
            html.Hr(),
            
            # Video grid
            html.Div([
                html.Div([
                    html.Div([
                        html.Iframe(
                            src="https://www.youtube.com/embed/ZlCDLAKmKpQ?si=ikzhBzGBHRfmN322",
                            style={"width": "70%", "height": "250px", "border-radius": "16px"},
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        ),
                        html.Div(
                            html.P("The BEST NBA Plays of the 2024 Season ! 🔥", className="ms-5 mt-1 px-1"),
                            style={"width": "100%"}
                        )
                    ], className="d-flex")
                ], className="mb-4"),
                html.Hr(),
                html.Div([
                    html.Div([
                        html.Iframe(
                            src="https://www.youtube.com/embed/ua-xR4SFXAs?si=S2Ecz_iXaW7OH6VM",
                            style={"width": "70%", "height": "250px", "border-radius": "16px"}
                        ),
                        html.Div(
                            html.P("The Top 100 Plays of the 2024 NBA Season 🔥", className="ms-5 mt-1 px-1"),
                            style={"width": "100%"}
                        )
                    ], className="d-flex")
                ], className="mb-4"),
                html.Hr(),
                html.Div([
                    html.Div([
                        html.Iframe(
                            src="https://www.youtube.com/embed/tq1-3aMtcFo?si=UYurNIgwKoURFK0h",
                            style={"width": "70%", "height": "250px", "border-radius": "16px"}
                        ),
                        html.Div(
                            html.P("30 Minutes of Stephen Curry BUCKETS | 2023-24 NBA Highlights", className="ms-5 mt-1 px-1"),
                            style={"width": "100%"}
                        )
                    ], className="d-flex")
                ], className="mb-4"),
            ], className="d-flex flex-column ms-5"),
            html.Hr(),
        ], className="box-shadow container bg-white p-4 mb-4"),
        
        # NBA News Feed
        html.Div([
            html.H2("Latest NBA News", className="mb-3"),
            html.Div(id="nba-news-feed", className="news-feed"),
        ], className="box-shadow container bg-white p-4 mb-4"),
        
        # Fan Poll
        # html.Div([
        #     html.H2("Fan Poll", className="mb-3"),
        #     html.P("Who do you think will win the NBA championship this year?"),
        #     dcc.RadioItems(
        #         id='championship-poll',
        #         options=[
        #             {'label': 'Boston Celtics', 'value': 'BOS'},
        #             {'label': 'Milwaukee Bucks', 'value': 'MIL'},
        #             {'label': 'Phoenix Suns', 'value': 'PHX'},
        #             {'label': 'Golden State Warriors', 'value': 'GSW'},
        #             {'label': 'Other', 'value': 'OTH'}
        #         ],
        #         className="my-3"
        #     ),
        #     html.Button('Submit', id='submit-poll', n_clicks=0, className="btn btn-primary"),
        #     html.Div(id='poll-results', className="mt-3")
        # ], className="box-shadow container bg-white p-4 mb-4"),
    ])