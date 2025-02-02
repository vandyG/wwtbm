import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import time

# Sample quiz data
questions = [
    {"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin", "Madrid"], "answer": "Paris"},
    {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Saturn"], "answer": "Mars"},
    {"question": "Who wrote 'To Kill a Mockingbird'?", "options": ["Harper Lee", "Mark Twain", "J.K. Rowling", "Ernest Hemingway"], "answer": "Harper Lee"},
]

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Who Wants to Be a Millionaire Quiz"

# Layout of the app
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Who Wants to Be a Millionaire", className="text-center text-warning mb-4"),
                        html.Div(id="question-section", className="mb-4"),
                        dbc.Button("Next Question", id="next-question-btn", color="success", className="me-2"),
                        dbc.Button("Previous Question", id="prev-question-btn", color="warning", className="me-2"),
                        html.Div(id="timer", className="mt-3 text-danger"),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.H3("Leaderboard", className="text-center text-primary mb-3"),
                        html.Div(id="leaderboard-section", className="mb-4"),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.H3("Quiz Analytics", className="text-center text-info mb-3"),
                        dcc.Graph(id="quiz-analytics"),
                    ],
                    width=3,
                ),
            ]
        ),
        dcc.Interval(id="timer-interval", interval=1000, n_intervals=0),
        dcc.Store(id="current-question-index", data=0),
        dcc.Store(id="quiz-responses", data={}),
    ],
    fluid=True,
    className="p-5 bg-dark text-white",
)

# Callback to update the question section
@app.callback(
    Output("question-section", "children"),
    Input("current-question-index", "data"),
)
def update_question_section(current_question_index):
    question_data = questions[current_question_index]
    return [
        html.H4(f"Question {current_question_index + 1}", className="text-warning"),
        html.P(question_data["question"], className="lead"),
        dbc.ListGroup(
            [
                dbc.ListGroupItem(option, className="mb-2") for option in question_data["options"]
            ]
        ),
    ]

# Callback to update the leaderboard
@app.callback(
    Output("leaderboard-section", "children"),
    Input("quiz-responses", "data"),
)
def update_leaderboard(responses):
    # Sample leaderboard data (replace with real logic)
    leaderboard_data = [
        {"name": "Player 1", "score": 10},
        {"name": "Player 2", "score": 8},
        {"name": "Player 3", "score": 5},
    ]
    return dbc.ListGroup(
        [
            dbc.ListGroupItem(f"{player['name']}: {player['score']} points", className="mb-2")
            for player in leaderboard_data
        ]
    )

# Callback to update the quiz analytics
@app.callback(
    Output("quiz-analytics", "figure"),
    Input("quiz-responses", "data"),
)
def update_quiz_analytics(responses):
    # Sample analytics data (replace with real logic)
    analytics_data = {
        "Correct": 5,
        "Incorrect": 3,
    }
    fig = px.pie(
        names=list(analytics_data.keys()),
        values=list(analytics_data.values()),
        title="Quiz Performance",
    )
    return fig

# Callback to handle next/previous question navigation
@app.callback(
    Output("current-question-index", "data"),
    Input("next-question-btn", "n_clicks"),
    Input("prev-question-btn", "n_clicks"),
    State("current-question-index", "data"),
    prevent_initial_call=True,
)
def navigate_questions(next_clicks, prev_clicks, current_question_index):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_question_index
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "next-question-btn" and current_question_index < len(questions) - 1:
        return current_question_index + 1
    elif button_id == "prev-question-btn" and current_question_index > 0:
        return current_question_index - 1
    return current_question_index

# Callback to update the timer
@app.callback(
    Output("timer", "children"),
    Input("timer-interval", "n_intervals"),
    State("current-question-index", "data"),
)
def update_timer(n_intervals, current_question_index):
    time_left = 30 - (n_intervals % 30)  # 30-second timer for each question
    if time_left == 0:
        return html.H4("Time's up!", className="text-danger")
    return html.H4(f"Time left: {time_left} seconds", className="text-warning")

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)