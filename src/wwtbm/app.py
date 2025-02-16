import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, no_update, dcc, html, State, callback_context


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
                                        "Question Statistics",
                                        style={"backgroundColor": "#1a1a1a", "color": "#FFD700"},
                                    ),
                                    dbc.CardBody(
                                        html.Div(
                                            [
                                                html.H4(
                                                    "Visualization Area",
                                                    style={"color": "#FFD700", "textAlign": "center"},
                                                ),
                                                html.P(
                                                    "Statistical visualizations for current question will appear here.",
                                                    style={"color": "#ffffff", "textAlign": "center"},
                                                ),
                                            ],
                                            id="visualization-container",
                                            style={
                                                "height": "400px",
                                                "display": "flex",
                                                "flexDirection": "column",
                                                "justifyContent": "center",
                                            },
                                        ),
                                        style={"backgroundColor": "#2a2a2a"},
                                    ),
                                ],
                            ),
                        ),
                    ),
                    dcc.Store(id="current-question-index", data=0),
                    dcc.Store(id="time-up", data=False),  # New store for tracking timer state
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

    # Sample questions and options with correct answers
    questions = [
        "What is the capital city of France?",
        "Which planet is known as the Red Planet?",
        "What is the largest mammal on Earth?",
    ]
    options = {
        0: [("A", "Paris"), ("B", "London"), ("C", "Berlin"), ("D", "Madrid")],
        1: [("A", "Mars"), ("B", "Venus"), ("C", "Jupiter"), ("D", "Saturn")],
        2: [("A", "Blue Whale"), ("B", "African Elephant"), ("C", "Giraffe"), ("D", "Hippopotamus")],
    }
    correct_answers = {0: "A", 1: "A", 2: "A"}  # Stores the correct option letter for each question

    # Callback to update the timer and trigger answer reveal
    @app.callback(
        [
            Output("timer-display", "children"),
            Output("bg-audio", "loop"),
            Output("bg-audio", "src"),
            Output("time-up", "data"),
        ],
        Input("timer-interval", "n_intervals"),
    )
    def update_timer(n_intervals):
        time_left = 30 - (n_intervals % 30)
        if time_left == 30 and n_intervals != 0:
            return (
                html.H2("Time's up!", className="text-danger"),
                False,
                app.get_asset_url("226000-9027b0d6-7a4f-4ee7-946f-6d011370681f.mp3"),
                True,
            )
        return html.H2(f"{time_left}", className="text-warning"), no_update, no_update, False

    # Callback to update question and options
    @app.callback(
        [Output("question-text", "children"), Output("options-grid", "children")],
        [Input("current-question-index", "data"), Input("time-up", "data")],
    )
    def update_question_and_options(current_index, time_up):
        # Get current question and options
        question = questions[current_index]
        current_options = options[current_index]
        correct_answer = correct_answers[current_index]

        def create_option_div(option_letter, option_text):
            # Determine if this option should be highlighted
            background_color = "#008000" if time_up and option_letter == correct_answer else "inherit"

            return html.Div(
                html.Span(f"{option_letter}: {option_text}"),
                className="hex-shape option-box",
                style={"backgroundColor": background_color} if time_up else {},
            )

        # Create options grid
        options_grid = [
            # First row of options (A and B)
            dbc.Row(
                [
                    dbc.Col(
                        create_option_div(current_options[0][0], current_options[0][1]),
                        width=6,
                    ),
                    dbc.Col(
                        create_option_div(current_options[1][0], current_options[1][1]),
                        width=6,
                    ),
                ],
            ),
            # Second row of options (C and D)
            dbc.Row(
                [
                    dbc.Col(
                        create_option_div(current_options[2][0], current_options[2][1]),
                        width=6,
                    ),
                    dbc.Col(
                        create_option_div(current_options[3][0], current_options[3][1]),
                        width=6,
                    ),
                ],
            ),
        ]

        return question, options_grid

        # Callback to handle next/previous question navigation

    @app.callback(
        Output("current-question-index", "data"),
        Input("next-question-btn", "n_clicks"),
        Input("prev-question-btn", "n_clicks"),
        State("current-question-index", "data"),
        prevent_initial_call=True,
    )
    def navigate_questions(next_clicks, prev_clicks, current_question_index):
        ctx = callback_context
        if not ctx.triggered:
            return current_question_index
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "next-question-btn" and current_question_index < len(questions) - 1:
            return current_question_index + 1
        if button_id == "prev-question-btn" and current_question_index > 0:
            return current_question_index - 1
        return current_question_index

    app.run_server(debug=debug)


if __name__ == "__main__":
    run_app(debug=True)
