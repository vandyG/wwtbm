import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import random

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Sample questions in increasing difficulty order
questions = [
    {"question": "What is the capital of France?", "options": ["Berlin", "Madrid", "Paris", "Rome"], "answer": "Paris"},
    {"question": "What is 5 + 7?", "options": ["10", "12", "14", "16"], "answer": "12"},
    {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": "Mars"},
]

prizes = ["$100", "$200", "$500"]
current_question_index = 0

# Card style for "Who Wants to Be a Millionaire?" layout
def get_question_card(question):
    return dbc.Card(
        dbc.CardBody([
            html.H4(question, className="card-title", style={"textAlign": "center", "color": "white"}),
        ]),
        style={"marginBottom": "20px", "backgroundColor": "#001f3f", "borderRadius": "15px", "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.5)"},
    )

def get_option_card(option, option_id):
    return dbc.Card(
        dbc.CardBody([
            dbc.RadioItems(
                options=[{"label": option, "value": option}],
                id=option_id,
                inline=False,
                style={"color": "white"}
            )
        ]),
        style={"margin": "10px auto", "backgroundColor": "#001f3f", "borderRadius": "10px", "boxShadow": "0px 3px 6px rgba(0, 0, 0, 0.3)", "padding": "15px"}
    )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Who Wants to Be a Millionaire?", style={"textAlign": "center", "color": "gold"}), width=12)
    ]),
    dbc.Row([
        dbc.Col(id="question-container", width=12)
    ]),
    dbc.Row([
        dbc.Col(id="options-container", width=12)
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Button("Submit", id="submit-button", color="warning", n_clicks=0, style={"width": "100%", "marginTop": "20px"}),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(id="feedback", width=12, style={"textAlign": "center", "color": "lime", "marginTop": "10px"})
    ]),
    dbc.Row([
        dbc.Col(id="prize", width=12, style={"textAlign": "center", "color": "gold", "marginTop": "20px"})
    ]),
    dbc.Row([
        dbc.Col(html.Div("Lifelines: 50/50 | Phone a Friend | Ask the Audience", style={"textAlign": "center", "color": "cyan", "marginTop": "20px"}), width=12)
    ]),
], style={"padding": "20px", "backgroundColor": "black", "minHeight": "100vh"})

@app.callback(
    [Output("question-container", "children"),
     Output("options-container", "children"),
     Output("prize", "children")],
    [Input("submit-button", "n_clicks")],
    [State("options-container", "children")]
)
def update_question(n_clicks, selected_option):
    global current_question_index
    if current_question_index >= len(questions):
        return "Congratulations! You've won!", "", "Total Prize: " + prizes[-1]

    q = questions[current_question_index]
    options = dbc.Row([
        dbc.Col(get_option_card(opt, f"option-{i}"), width=6) for i, opt in enumerate(q["options"])
    ], justify="center")

    current_prize = f"Current Prize: {prizes[current_question_index]}"

    return get_question_card(q["question"]), options, current_prize

if __name__ == "__main__":
    app.run_server(debug=True)
