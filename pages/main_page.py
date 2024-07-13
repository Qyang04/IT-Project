from dash import html, dcc, dash_table
import plotly.express as px
import pickle

# Load your data here
with open('data/processed_data.pkl', 'rb') as f:
    data = pickle.load(f)

predictions_with_details = data['predictions_with_details']
accuracy = data['accuracy']
correct_count = data['correct_count']
incorrect_count = data['incorrect_count']

def main_page_content():
    return html.Div([
        html.H1("NBA Game Prediction Dashboard"),
        html.H2("Model Accuracy"),
        html.Div(f"{accuracy:.2%}", className="accuracy-display"),
        
        dcc.Graph(
            id='prediction-pie-chart',
            figure=px.pie(
                names=['Correct', 'Incorrect'],
                values=[correct_count, incorrect_count],
                title='Prediction Accuracy',
                color_discrete_sequence=['#00CC96', '#EF553B']
            ),
            style={'height': '400px'}
        ),
        
        html.H2("Prediction Results"),
        dash_table.DataTable(
            id='prediction-table',
            columns=[
                {"name": "Date", "id": "date"},
                {"name": "Teams", "id": "teams"},
                {"name": "Actual Result", "id": "actual"},
                {"name": "Predicted Result", "id": "prediction"},
                {"name": "Correct?", "id": "correct"}
            ],
            data=[
                {
                    "date": row["date"],
                    "teams": f"{row['team']} vs {row['team_opp']}",
                    "actual": row["actual"],
                    "prediction": row["prediction"],
                    "correct": "Yes" if row["correct"] else "No"
                }
                for row in predictions_with_details.to_dict('records')
            ],
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'left',
                'padding': '10px',
                'font-family': 'Arial, sans-serif',
                'font-size': '14px'
            },
            style_header={
                'backgroundColor': '#f2f2f2',
                'fontWeight': 'bold',
                'border': '1px solid #ddd'
            },
            style_data={
                'border': '1px solid #ddd'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f9f9f9'
                },
                {
                    'if': {'filter_query': '{correct} eq "Yes"'},
                    'backgroundColor': 'rgb(220, 249, 227)',
                    'color': 'black'
                },
                {
                    'if': {'filter_query': '{correct} eq "No"'},
                    'backgroundColor': 'rgb(255, 236, 236)',
                    'color': 'black'
                }
            ],
            page_action='native',
            page_size=20,
            sort_action='native',
            filter_action='native'
        )
    ])