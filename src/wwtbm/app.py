import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, no_update, dcc, html


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
                                html.Div(
                                    html.Span("What is the capital city of France?"),
                                    className="hex-shape question-box mt-4",
                                    style={"fontSize": "30px", "textAlign": "center"},
                                ),
                                # Options grid
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Div(
                                                        html.Span(f"{opt[0]}: {opt[1]}"),
                                                        className="hex-shape option-box",
                                                    ),
                                                    width=6,
                                                )
                                                for opt in [("A", "Paris"), ("B", "London")]
                                            ],
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Div(
                                                        html.Span(f"{opt[0]}: {opt[1]}"),
                                                        className="hex-shape option-box",
                                                    ),
                                                    width=6,
                                                )
                                                for opt in [("C", "Berlin"), ("D", "Madrid")]
                                            ],
                                        ),
                                    ],
                                    id="optoins-grid",
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
                                width=6,  # Ensure the column has a width
                            ),
                        ],
                        style={"display": "flex", "flexWrap": "wrap"},  # Allow wrapping on smaller screens
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

    # TODO: Fetch Questions.
    questions = ["What is the capital city of France?"]
    options = {0: ["Paris", "London", "Madrid", "Berlin"]}

    # Callback to update the timer
    @app.callback(
        Output("timer-display", "children"),
        Output("bg-audio", "loop"),
        Output("bg-audio", "src"),
        Input("timer-interval", "n_intervals"),
    )
    def update_timer(n_intervals):
        time_left = 30 - (n_intervals % 30)  # 30-second timer for each question
        if time_left == 30 and n_intervals != 0:
            return (
                (html.H2("Time's up!", className="text-danger"),),
                False,
                app.get_asset_url("226000-9027b0d6-7a4f-4ee7-946f-6d011370681f.mp3"),
            )
        return html.H2(f"{time_left}", className="text-warning"), no_update, no_update

    # @app.callback(Output)
    # def update_question_section(current_question_index):
    #     question_data = questions[current_question_index]
    #     return [
    #         html.H4(f"Question {current_question_index + 1}", className="text-warning"),
    #         html.P(question_data["question"], className="lead"),
    #         dbc.ListGroup([dbc.ListGroupItem(option, className="mb-2") for option in question_data["options"]]),
    #     ]

    app.run_server(debug=debug)


if __name__ == "__main__":
    run_app(debug=True)
