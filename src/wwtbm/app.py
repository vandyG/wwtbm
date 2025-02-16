import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, no_update, dcc, html, State, callback_context
import pandas as pd
import plotly.graph_objects as go
from fetch import get_question_data,get_answer_data
from visualisation import get_user_performance_graph,get_answer_distribution_graph

def create_game_layout(app: Dash):
    return html.Div(
        [
            # Logo
            html.Div(
                html.Img(src=app.get_asset_url("WWTBAMUS2020Logo.webp"), style={"height": "20%", "width": "20%"}),
                style={"textAlign": "center"},
            ),
            # Main container
            dbc.Container(
                [
                    # Question and Options
                    dbc.Row(
                        dbc.Col(
                            [
                                # Question component
                                html.Div(
                                    html.Span(id="question-text"),
                                    className="hex-shape question-box mt-4",
                                    style={"fontSize": "30px", "textAlign": "center"},
                                ),
                                # Options grid
                                html.Div(
                                    id="options-grid",
                                    style={"marginTop": "20px", "fontSize": "24px"},
                                ),
                            ],
                        ),
                    ),
                    # Timer and Controls
                    dbc.Row(
                        [
                            # Timer Column
                            dbc.Col(
                                [
                                    html.Div(html.Span("Timer"), className="hex-shape question-box mb-0 mt-4"),
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                html.H2(
                                                    "30",
                                                    id="timer-display",
                                                    style={
                                                        "color": "#FFD700",
                                                        "textAlign": "center",
                                                        "fontSize": "48px",
                                                    },
                                                ),
                                            ),
                                        ],
                                        style={"backgroundColor": "#00003B"},
                                    ),
                                ],
                                width=6,
                            ),
                            # Control Buttons
                            dbc.Col(
                                html.Div(
                                    [
                                        html.Button(html.Span(text), className="hex-shape hex-button", id=f"{id_}-btn")
                                        for text, id_ in [
                                            ("Previous", "prev-question"),
                                            ("Next", "next-question"),
                                        ]
                                    ],
                                    className="controls-container mt-4",
                                    style={
                                        "display": "flex",
                                        "justifyContent": "center",
                                        "gap": "20px",
                                    },
                                ),
                                width=6,
                            ),
                        ],
                        style={"display": "flex", "flexWrap": "wrap"},
                    ),
                    # Statistics Section
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        "Answer Distribution",
                                        style={"backgroundColor": "#1a1a1a", "color": "#FFD700"},
                                    ),
                                    dbc.CardBody(
                                        html.Div(
                                            id="visualization-container",
                                            style={
                                                "height": "400px",
                                                "backgroundColor": "#2a2a2a",
                                            },
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ),
                    dcc.Store(id="current-question-index", data=1),
                    dcc.Store(id="time-up", data=False),
                    dcc.Store(id="question-data", data=None),
                    dcc.Store(id="answer-data", data=None),
                    dcc.Interval(
                        id="timer-interval",
                        interval=1000,
                        n_intervals=0,
                        max_intervals=30,
                    ),
                ],
                fluid=True,
            ),
            html.Audio(
                src=app.get_asset_url("226000-66fa2379-b277-4480-a2bc-feeb689bd09b.mp3"),
                hidden=False,
                autoPlay=True,
                loop=True,
                id="bg-audio",
            ),
        ],
        style={"backgroundColor": "#00003B", "minHeight": "100vh", "padding": "20px"},
    )

def run_app(debug=False):
    app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], assets_folder="assets")
    app.layout = create_game_layout(app=app)
    df_questions = get_question_data()
    @app.callback(
    [
        Output("question-data", "data"),
        Output("answer-data", "data"),
        Output("timer-display", "children"),
        Output("bg-audio", "loop"),
        Output("bg-audio", "src"),
        Output("time-up", "data"),
    ],
    [
        Input("timer-interval", "n_intervals"),
    ]
)
    def update_data_and_timer(n_intervals):
        # Initial Load: Fetch Questions
        if n_intervals == 0:
            print("reading question")
            return (
                df_questions.to_dict("records"),
                no_update,
                html.H2("30", className="text-warning"),  # Timer starts at 30
                no_update,
                no_update,
                False,
            )

        # Timer Countdown
        time_left = 30 - (n_intervals % 30)

        # Timer runs out
        if time_left == 30 and n_intervals != 0:
            print("reading answers")
            df_answers = get_answer_data()
            return (
                no_update,
                df_answers.to_dict("records"),  # Update answer data
                html.H2("Time's up!", className="text-danger"),  # Timer display update
                False,  # Stop looping background audio
                app.get_asset_url("226000-9027b0d6-7a4f-4ee7-946f-6d011370681f.mp3"),  # Change audio
                True,  # Set time-up flag to True
            )
        # Default case: Just update timer
        return (
            no_update,
            no_update,
            html.H2(f"{time_left}", className="text-warning"),
            no_update,
            no_update,
            False,
        )
    @app.callback(
        [
            Output("current-question-index", "data"),
            Output("timer-interval", "n_intervals"),
        ],
        [
            Input("next-question-btn", "n_clicks"),
            Input("prev-question-btn", "n_clicks"),
            Input("question-data", "data"),
        ],
        [State("current-question-index", "data")],
        prevent_initial_call=True, 
        
        
        
    )
    def navigate_question(next_clicks, prev_clicks,question_data,current_index):

        max_index = len(question_data)
        ctx = callback_context
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
        if not question_data:
            return no_update, no_update
        
        if triggered_id == "next-question-btn" and current_index < max_index:
            print("CLICKED NEXT and updated timer")
            return (
                current_index + 1,
                0,  # Reset n_intervals
            )

        # Handle Previous Question Click
        if triggered_id == "prev-question-btn" and current_index > 1:
            print("CLICKED prev")
            return (
                current_index - 1,
                no_update,
            )

    @app.callback(
        [Output("question-text", "children"), Output("options-grid", "children"), Output("visualization-container", "children")],
        [Input("current-question-index", "data"), Input("time-up", "data")],
        [State("question-data", "data"), State("answer-data", "data")]
    )
    def update_question_and_options(current_index, time_up, question_data, answer_data):
        if not question_data:
            return no_update, no_update, no_update

        df_questions = pd.DataFrame(question_data).reset_index(drop=True).set_index("Number")

        current_question = df_questions.loc[current_index]

        options = [
            ("1", current_question["Option1"]),
            ("2", current_question["Option2"]),
            ("3", current_question["Option3"]),
            ("4", current_question["Option4"]),
        ]
        
        def create_option_div(option_letter, option_text):

            if bool(time_up) and int(option_letter) == current_question["Answer"]:
                print("205")
            background_color = "#008000" if time_up and int(option_letter) == current_question["Answer"] else "inherit"
            
            
            return html.Div(
                html.Span(f"{option_letter}: {option_text}"),
                className="hex-shape option-box",
                style={"backgroundColor": background_color} if time_up else {},
            )

        # Create options grid
        options_grid = [
            dbc.Row([
                dbc.Col(create_option_div(options[0][0], options[0][1]), width=6),
                dbc.Col(create_option_div(options[1][0], options[1][1]), width=6),
            ]),
            dbc.Row([
                dbc.Col(create_option_div(options[2][0], options[2][1]), width=6),
                dbc.Col(create_option_div(options[3][0], options[3][1]), width=6),
            ]),
        ]

        # Create visualization when time is up

        visualization = []
        if answer_data:

            df_answers = pd.DataFrame(answer_data)

            fig = get_user_performance_graph(df_answers, 5)
            visualization = [dcc.Graph(figure=fig, style={"height": "100%"})]

        return current_question["Question"], options_grid, visualization


    app.run_server(debug=debug)

if __name__ == "__main__":
    run_app(debug=True)