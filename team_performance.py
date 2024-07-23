html.H2("Team Performance Over Time"),
    dcc.Dropdown(
        id='team-dropdown',
        options=[{'label': team, 'value': team} for team in df['team'].unique()],
        value=df['team'].iloc[0],
        style={'width': '50%'}
    ),
    dcc.Graph(id='team-performance-graph')
    
    
# Callback to update the team performance graph
@app.callback(
    Output('team-performance-graph', 'figure'),
    Input('team-dropdown', 'value')
)
def update_graph(selected_team):
    team_data = df[df['team'] == selected_team].sort_values('date')
    fig = px.line(team_data, x='date', y='won', title=f'{selected_team} Performance Over Time')
    return fig