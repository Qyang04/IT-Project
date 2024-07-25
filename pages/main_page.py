# pages/main_page.py
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
        html.Div([
            html.H1("NBA Game Prediction Dashboard", className="mb-4 text-center"),
            html.H2("Model Accuracy", className="mb-3"),
            html.Div(f"{accuracy:.2%}", className="accuracy-display mb-4"),
            
            dcc.Graph(
                id='prediction-pie-chart',
                figure=px.pie(
                    names=['Correct', 'Incorrect'],
                    values=[correct_count, incorrect_count],
                    title='Prediction Accuracy',
                    color_discrete_sequence=['#9290C3', '#535C91']
                )
            )
        ], className="box-shadow container bg-white p-4 mb-4"),
        
        html.Div([
            html.Div([
                html.Div([
                    html.H2("Total Data Used", className="h4"),
                    html.Div(f"{correct_count+incorrect_count}", className="box-value")
                ], className="box-shadow bg-white py-5 h-100 text-center")
            ], className="col-lg-4 mb-3 mb-lg-0"),
            html.Div([
                html.Div([
                    html.H2("Total Correct Prediction", className="h4"),
                    html.Div(f"{correct_count}", className="box-value correct")
                ], className="box-shadow bg-white py-5 h-100 text-center")
            ], className="col-lg-4 mb-3 mb-lg-0"),
            html.Div([
                html.Div([
                    html.H2("Total Incorrect Prediction", className="h4"),
                    html.Div(f"{incorrect_count}", className="box-value incorrect")
                ], className="box-shadow bg-white py-5 h-100 text-center")
            ], className="col-lg-4 mb-3 mb-lg-0")
        ], className="row mb-4"),
        
        html.Div([
            html.H2("Prediction Results", className="text-center"),
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
                style_table={
                    'overflowX': 'auto',
                    'border': '1px solid #7895CB',
                    'border-radius': '12px',
                    'box-shadow': '0 0 10px rgba(0,0,0,0.1)',
                    'margin-bottom': '5px'
                },
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'font-family': 'Arial, sans-serif',
                    'font-size': '14px',
                    'borderLeft': 'none',
                    'borderRight': 'none',
                    'borderTop': '1px solid #7895CB',
                    'borderBottom': '1px solid #7895CB',
                    'backgroundColor': '#E1FFEE'
                },
                style_header={
                    'backgroundColor': '#A0BFE0',
                    'fontWeight': 'bold',
                    'border': 'none'
                },
                style_filter={
                    'borderTop': '1px solid #7895CB'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': '#C5DFF8'
                    },
                    {
                        'if': {'filter_query': '{correct} eq "Yes"'},
                        'color': 'black'
                    },
                    {
                        'if': {'filter_query': '{correct} eq "No"'},
                        'color': 'black'
                    }
                ],
                page_action='native',
                page_size=15,
                sort_action='native',
                filter_action='native'
            )
        ], className="box-shadow container bg-white p-4 mb-4")
    ])