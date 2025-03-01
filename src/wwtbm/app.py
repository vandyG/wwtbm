from dataclasses import dataclass
from typing import List, Tuple

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, callback_context, dcc, html, no_update

from wwtbm.fetch import get_answer_data
from wwtbm.question_visualisation import *
from wwtbm.visualisation import get_answer_distribution_graph, get_user_performance_graph


@dataclass
class GameTheme:
    primary: str = "#000066"
    secondary: str = "#4169E1"
    background: str = "#00003B"
    text: str = "#FFFFFF"
    accent: str = "#FFD700"
    success: str = "#008000"
    card_bg: str = "#2a2a2a"
    header_bg: str = "#1a1a1a"

    def get_modal_style(self):
        return {"backgroundColor": self.primary, "border": f"1px solid {self.secondary}"}

    def get_card_style(self):
        return {"backgroundColor": self.card_bg, "border": f"1px solid {self.secondary}", "color": self.text}

    def get_header_style(self):
        return {"backgroundColor": self.header_bg, "color": self.accent}


class GameData:
    def __init__(self):
        self.questions = [
            "What’s the biggest fear of an iPhone user?",
            "Which type of milk is NOT real milk?",
            "What magical ingredient in coffee turns zombies into functioning humans every morning?",
            "What is the Iris dataset most commonly used for?",
            "What’s the best way to find your gate on AIRPORT?",
            "Which city is home to Hollywood??",
        ]
        self.options = {
            0: [
                ("A", "Running out of storage"),
                ("B", 'Seeing the "low battery" warning at 10%'),
                ("C", "Dropping their phone and praying it survived"),
                ("D", "All of the above"),
            ],
            1: [
                ("A", "Cow milk"),
                ("B", "Oat milk"),
                ("C", "Soy milk"),
                ("D", "iMilk (Apple’s latest product)"),
            ],
            2: [
                ("A", "Sugar"),
                ("B", "Caffeine"),
                ("C", "Hope"),
                ("D", "Pure willpower"),
            ],
            3: [
                ("A", "Identifying flowers"),
                ("B", "Training AI to take over the world"),
                ("C", "Confusing beginners in machine learning"),
                ("D", "Teaching pandas (the Python library, not the bear) new tricks"),
            ],
            4: [
                ("A", "Follow the herd"),
                ("B", "Ask someone who looks equally lost"),
                ("C", "Pray"),
                ("D", "Walk forever"),
            ],
            5: [
                ("A", "Los Angeles"),
                ("B", "San Francisco"),
                ("C", "Las Vegas"),
                ("D", "Miami"),
            ],
        }
        self.correct_answers = {
            0: "D",
            1: "D",
            2: "B",
            3: "A",
            4: "B",
            5: "A",
        }
        self.answer_points = {
            1: 1000,
            2: 8000,
            3: 32000,
            4: 500000,
            5: 1000000,
        }
        self.answer_data = None

    def update_answer_data(self):
        self.answer_data = get_answer_data()


def create_option_div(
    option_letter: str, option_text: str, correct_answer: str, time_up: bool, theme: GameTheme
) -> html.Div:
    style = {"backgroundColor": theme.success if time_up and option_letter == correct_answer else "inherit"}
    return html.Div(
        html.Span(f"{option_letter}: {option_text}"),
        className="hex-shape option-box",
        style=style if time_up else {},
    )


def create_options_grid(
    options: list[tuple[str, str]], correct_answer: str, time_up: bool, theme: GameTheme
) -> list[dbc.Row]:
    return [
        dbc.Row(
            [
                dbc.Col(create_option_div(options[i][0], options[i][1], correct_answer, time_up, theme), width=6),
                dbc.Col(
                    create_option_div(options[i + 1][0], options[i + 1][1], correct_answer, time_up, theme), width=6
                ),
            ],
        )
        for i in (0, 2)
    ]


def create_modals(theme: GameTheme) -> list[dbc.Modal]:
    modal_style = theme.get_modal_style()
    header_style = {"border": f"1px solid {theme.secondary}"}

    question_modal = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Header"), style=header_style),
            dbc.ModalBody(
                dbc.Tabs(
                    style={
                        "--bs-nav-tabs-border-color": theme.secondary,
                        "--bs-nav-link-hover-color": theme.secondary,
                        "--bs-nav-tabs-link-active-border-color": f"{theme.secondary} {theme.secondary} transparent",
                        "--bs-nav-tabs-link-active-bg": theme.primary,
                    },
                    id="visualization-tabs",
                )
            ),
        ],
        id="modal-question",
        size="xl",
        is_open=False,
        content_style=modal_style,
    )

    answer_modal = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Header"), style=header_style),
            dbc.ModalBody(id="visualisation-answer"),
        ],
        id="modal-answer",
        size="xl",
        is_open=False,
        content_style=modal_style,
    )

    return [question_modal, answer_modal]


def create_leaderboard(leader_data: dict[str, int], theme: GameTheme) -> dbc.CardBody:
    return dbc.Table(
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td(
                            f"{rank + 1}",
                            className="text-center",
                            colSpan=1,
                        ),
                        html.Td(
                            f"{leader[0]}",
                            className="text-center",
                            colSpan=3,
                        ),
                        html.Td(
                            f"${leader[1]}",
                            className="text-center",
                            colSpan=2,
                        ),
                    ],
                )
                for rank, leader in enumerate(leader_data.items())
            ],
        ),
        bordered=False,
        dark=True,
        responsive=True,
        style={
            "color": theme.text,
            "--bs-table-bg": theme.background,
            "--bs-table-border-color": theme.secondary,
        },
    )


def create_statistics_card(fig, theme: GameTheme) -> dbc.Col:
    return dbc.CardBody(
        [
            dcc.Graph(
                figure=fig,
                style={"backgroundColor": "inherit"},
            ),
        ],
    )


def create_game_layout(app: Dash, theme: GameTheme) -> html.Div:
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
                    # [Previous question and options section remains the same]
                    dbc.Row(
                        dbc.Col(
                            [
                                html.Div(
                                    html.Span(id="question-text"),
                                    className="hex-shape question-box mt-4",
                                    style={"fontSize": "30px", "textAlign": "center"},
                                    id="question-section",
                                ),
                                html.Div(id="options-grid", style={"marginTop": "20px", "fontSize": "24px"}),
                            ]
                        )
                    ),
                    # [Previous timer and controls section remains the same]
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(
                                        html.Span("Timer"),
                                        className="hex-shape question-box mb-0 mt-4",
                                        style={"fontSize": "30px"},
                                    ),
                                    dbc.Card(
                                        dbc.CardBody(
                                            html.H2(
                                                "30",
                                                id="timer-display",
                                                style={
                                                    "color": theme.accent,
                                                    "textAlign": "center",
                                                    "fontSize": "48px",
                                                },
                                            )
                                        ),
                                        style={"backgroundColor": theme.background},
                                    ),
                                ],
                                width=6,
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        html.Button(
                                            html.Span(text),
                                            className="hex-shape hex-button",
                                            id=f"{id_}-btn",
                                            style={"fontSize": "30px"},
                                        )
                                        for text, id_ in [("Previous", "prev-question"), ("Next", "next-question")]
                                    ],
                                    className="controls-container mt-4",
                                    style={"display": "flex", "justifyContent": "center", "gap": "20px"},
                                ),
                                width=6,
                            ),
                        ]
                    ),
                    # Leaderboard and Statistics Section
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(
                                        html.Span("Leaderboard"),
                                        className="hex-shape question-box mb-0 mt-4",
                                        style={"fontSize": "30px"},
                                    ),
                                    dbc.Card(
                                        dbc.CardBody(
                                            id="leaderboard-card-body",
                                            className="ms-4 me-4",
                                        ),
                                        style={"backgroundColor": "inherit"},
                                    ),
                                ],
                                width=4,
                            ),
                            dbc.Col(
                                [
                                    html.Div(
                                        html.Span("Statistics"),
                                        className="hex-shape question-box mb-0 mt-4",
                                        style={"fontSize": "30px"},
                                    ),
                                    dbc.Card(
                                        id="statistics-card",
                                        style={"backgroundColor": "inherit"},
                                    ),
                                ],
                                width=8,
                            ),
                        ],
                        className="mt-4",
                    ),
                    # [Previous game state storage remains the same]
                    dcc.Store(id="current-question-index", data=0),
                    dcc.Store(id="time-up", data=False),
                    dcc.Interval(id="timer-interval", interval=1000, n_intervals=0, max_intervals=30),
                    # Background audio
                    html.Audio(
                        src=app.get_asset_url("226000-66fa2379-b277-4480-a2bc-feeb689bd09b.mp3"),
                        id="bg-audio",
                        autoPlay=True,
                        loop=True,
                        hidden=False,
                    ),
                ],
                fluid=True,
            ),
            # Modals
            *create_modals(theme),
        ],
        style={"backgroundColor": theme.background, "minHeight": "100vh", "padding": "20px"},
    )


def init_callbacks(app: Dash, game_data: GameData, theme: GameTheme):
    @app.callback(
        [
            Output("timer-display", "children"),
            Output("bg-audio", "loop"),
            Output("bg-audio", "src"),
            Output("time-up", "data"),
            Output("timer-interval", "n_intervals"),
        ],
        [Input("timer-interval", "n_intervals"), Input("current-question-index", "data")],
    )
    def update_timer(n_intervals, question_index):
        ctx = callback_context
        if ctx.triggered_id == "current-question-index":
            return (
                html.H2("30", className="text-warning"),
                True,
                app.get_asset_url("226000-66fa2379-b277-4480-a2bc-feeb689bd09b.mp3"),
                False,
                0,
            )

        time_left = 30 - (n_intervals % 30)
        if time_left == 30 and n_intervals != 0:
            return (
                html.H2("Time's up!", className="text-danger"),
                False,
                app.get_asset_url("226000-9027b0d6-7a4f-4ee7-946f-6d011370681f.mp3"),
                True,
                n_intervals,
            )
        return html.H2(f"{time_left}", className="text-warning"), no_update, no_update, False, n_intervals

    @app.callback(
        [Output("question-text", "children"), Output("options-grid", "children")],
        [Input("current-question-index", "data"), Input("time-up", "data")],
    )
    def update_question_and_options(current_index, time_up):
        question = game_data.questions[current_index]
        current_options = game_data.options[current_index]
        correct_answer = game_data.correct_answers[current_index]
        return question, create_options_grid(current_options, correct_answer, time_up, theme)

    @app.callback(
        Output("current-question-index", "data"),
        [Input("next-question-btn", "n_clicks"), Input("prev-question-btn", "n_clicks")],
        State("current-question-index", "data"),
        prevent_initial_call=True,
    )
    def navigate_questions(next_clicks, prev_clicks, current_index):
        ctx = callback_context
        if not ctx.triggered:
            return current_index

        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "next-question-btn" and current_index < len(game_data.questions) - 1:
            return current_index + 1
        if button_id == "prev-question-btn" and current_index > 0:
            return current_index - 1
        return current_index

    @app.callback(
        [Output("modal-question", "is_open"), Output("visualization-tabs", "children")],
        Input("question-section", "n_clicks"),
        State("modal-question", "is_open"),
    )
    def toggle_question_modal(n_clicks, is_open):
        if n_clicks:
            figs = []
            fig = create_stock_line_chart()
            figs = [dcc.Graph(figure=fig, style={"height": "100%"})]
            return not is_open, figs
        return is_open, []

    @app.callback(
        [
            Output("modal-answer", "is_open"),
            Output("visualisation-answer", "children"),
            Output("options-grid", "n_clicks"),
        ],
        [Input("options-grid", "n_clicks"), Input("time-up", "data")],
        State("modal-answer", "is_open"),
    )
    def toggle_answer_modal(n_clicks, time_up, is_open):
        if n_clicks and time_up:
            return not is_open, [], no_update
        return no_update, no_update, 0

    @app.callback(
        Output("leaderboard-card-body", "children"),
        Output("statistics-card", "children"),
        Input("time-up", "data"),
    )
    def update_leaderboard(time_up):
        if time_up:
            game_data.update_answer_data()
            answer_data = game_data.answer_data
            points = game_data.answer_points
            answer_data["points"] = answer_data["Question"].map(points)
            leader_board = dict(
                sorted(
                    answer_data[answer_data["Correct"]].groupby("Name")["points"].sum().to_dict().items(),
                    key=lambda x: x[1],
                    reverse=True,
                ),
            )

            fig = get_user_performance_graph(answer_data, 5)
            fig.update_layout(plot_bgcolor=theme.background, paper_bgcolor=theme.background)
            return create_leaderboard(leader_board, theme), create_statistics_card(fig, theme)
        return no_update


def run_app(debug=False):
    app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], assets_folder="assets")
    theme = GameTheme()
    game_data = GameData()

    app.layout = create_game_layout(app, theme)
    init_callbacks(app, game_data, theme)
    app.run_server(debug=debug)


if __name__ == "__main__":
    run_app(debug=True)
