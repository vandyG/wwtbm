"""Who Wants to Be a Millionaire Game Dashboard.

This module implements an interactive Dash application that recreates the 'Who Wants to Be a Millionaire'
game show experience. It provides a complete web-based interface with question management, timer functionality,
visualizations, and leaderboards.

The application features:
- A question and multiple-choice answer display system
- Interactive timer with audio cues
- Data visualizations for each question
- Audience poll functionality
- Live leaderboard of player performance
- Statistical performance analysis

The module uses a combination of Dash components, Plotly visualizations, and Bootstrap styling
to create a responsive and engaging game interface.

Dependencies:
    - dash: Core framework for the web application
    - dash_bootstrap_components: Styling and layout components
    - plotly: For interactive visualizations
    - pandas: For data manipulation
    - dataclasses: For structured data objects
"""

from dataclasses import dataclass

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, callback_context, dcc, html, no_update
from pandas import DataFrame

import wwtbm.question_visualisation as qv
from wwtbm.fetch import get_answer_data
from wwtbm.visualisation import get_answer_distribution_graph, get_user_performance_graph


@dataclass
class GameTheme:
    """Defines the color theme and styling for the game interface.

    This dataclass provides a centralized way to manage colors and generate consistent
    styles for various UI components throughout the application.

    Attributes:
        primary (str): Primary color for main elements
        secondary (str): Secondary color for accents and highlights
        hover (str): Color for hover states
        background (str): Background color for the main application
        text (str): Text color
        accent (str): Accent color for special elements
        success (str): Color for correct answers and success states
        card_bg (str): Background color for cards
        header_bg (str): Background color for headers
    """

    primary: str = "#000066"
    secondary: str = "#4169E1"
    hover: str = "#000099"
    background: str = "#00003B"
    text: str = "#FFFFFF"
    accent: str = "#FFD700"
    success: str = "#008000"
    card_bg: str = "#2a2a2a"
    header_bg: str = "#1a1a1a"

    def get_modal_style(self) -> dict:
        """Generate the styling dictionary for modal dialogs.

        Returns:
            dict: CSS style dictionary for modal components
        """
        return {"backgroundColor": self.primary, "border": f"1px solid {self.secondary}"}

    def get_card_style(self) -> dict:
        """Generate the styling dictionary for card components.

        Returns:
            dict: CSS style dictionary for card components
        """
        return {"backgroundColor": self.card_bg, "border": f"1px solid {self.secondary}", "color": self.text}

    def get_header_style(self) -> dict:
        """Generate the styling dictionary for header components.

        Returns:
            dict: CSS style dictionary for header components
        """
        return {"backgroundColor": self.header_bg, "color": self.accent}


class GameData:
    """Manages the game data including questions, options, and player answers.

    This class centralizes all game content and provides methods to interact with
    and update the data during gameplay.

    Attributes:
        questions (list): List of game questions
        options (dict): Dictionary mapping question indices to option lists
        correct_answers (dict): Dictionary mapping question indices to correct answers
        answer_points (dict): Dictionary mapping question numbers to point values
        answer_data (DataFrame): Player answer data from external source
    """

    def __init__(self):
        """Initialize the game data with questions, options, and scoring information."""
        self.questions = [
            "1. What's the biggest fear of an iPhone user?",
            "2. What is the most persistent decoration on NYC statues and buildings?",
            "3. Which type of milk is NOT real milk?",
            "4. What is the Iris dataset most commonly used for?",
            "5. What's the best way to find your gate on AIRPORT?",
            "6. Which city is home to Hollywood??",
        ]
        self.options = {
            0: [
                ("A", "Running out of storage"),
                ("B", 'Seeing the "low battery" warning at 10%'),
                ("C", "Dropping their phone and praying it survived"),
                ("D", "All of the above"),
            ],
            2: [
                ("A", "Cow milk"),
                ("B", "Oat milk"),
                ("C", "Soy milk"),
                ("D", "iMilk (Apple's latest product)"),
            ],
            1: [
                ("A", "Graffiti mustaches"),
                ("B", "'I ❤️ NY' stickers"),
                ("C", "Lost tourist maps"),
                ("D", "Pfigeon Picasso painting"),
            ],
            3: [
                ("A", "Identifying flowers"),
                ("B", "Training AI to take over the world"),
                ("C", "Confusing beginners in machine learning"),
                ("D", "Teaching pandas new tricks"),
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
            2: "D",
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

    def update_answer_data(self) -> DataFrame:
        """Fetch and update the player answer data from external source.

        Returns:
            DataFrame: Updated answer data
        """
        self.answer_data = get_answer_data()


def create_option_div(
    option_letter: str,
    option_text: str,
    correct_answer: str,
    time_up: bool,  # noqa: FBT001
    theme: GameTheme,
) -> html.Div:
    """Create a styled div for an answer option.

    Args:
        option_letter (str): The option letter (A, B, C, or D)
        option_text (str): The text content of the option
        correct_answer (str): The letter of the correct answer
        time_up (bool): Whether the timer has expired
        theme (GameTheme): The game's theme object for styling

    Returns:
        html.Div: Styled div containing the answer option
    """
    style = {"backgroundColor": theme.success if time_up and option_letter == correct_answer else "inherit"}
    return html.Div(
        html.Span(f"{option_letter}: {option_text}"),
        className="hex-shape option-box",
        style=style if time_up else {},
    )


def create_options_grid(
    options: list[tuple[str, str]],
    correct_answer: str,
    time_up: bool,  # noqa: FBT001
    theme: GameTheme,
) -> list[dbc.Row]:
    """Create a grid layout of answer options.

    Args:
        options (list): List of tuples with (letter, text) for each option
        correct_answer (str): The letter of the correct answer
        time_up (bool): Whether the timer has expired
        theme (GameTheme): The game's theme object for styling

    Returns:
        list: List of Bootstrap rows containing the options
    """
    return [
        dbc.Row(
            [
                dbc.Col(create_option_div(options[i][0], options[i][1], correct_answer, time_up, theme), width=6),
                dbc.Col(
                    create_option_div(options[i + 1][0], options[i + 1][1], correct_answer, time_up, theme),
                    width=6,
                ),
            ],
        )
        for i in (0, 2)
    ]


def create_modals(theme: GameTheme) -> list[dbc.Modal]:
    """Create the modal dialogs for visualizations and audience poll.

    Args:
        theme (GameTheme): The game's theme object for styling

    Returns:
        list: List of Bootstrap modal components
    """
    modal_style = theme.get_modal_style()
    header_style = {"border": f"1px solid {theme.secondary}"}

    question_modal = dbc.Modal(
        [
            dbc.ModalHeader(style=header_style, id="modal-question-header"),
            dbc.ModalBody(
                dbc.Tabs(
                    style={
                        "--bs-nav-tabs-border-color": theme.secondary,
                        "--bs-nav-link-hover-color": theme.secondary,
                        "--bs-nav-tabs-link-active-border-color": f"{theme.secondary} {theme.secondary} transparent",
                        "--bs-nav-tabs-link-active-bg": theme.primary,
                    },
                    id="visualization-tabs",
                ),
            ),
        ],
        id="modal-question",
        size="xl",
        is_open=False,
        content_style=modal_style,
    )

    answer_modal = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Audience Poll"), style=header_style),
            dbc.ModalBody(
                id="visualisation-answer",
                class_name="p-5",
            ),
        ],
        id="modal-answer",
        size="xl",
        is_open=False,
        content_style=modal_style,
    )

    return [question_modal, answer_modal]


def create_modal_tabs(figures: dict, theme: GameTheme) -> list[dbc.Tab]:
    """Create tabs for the visualization modal.

    Args:
        figures (dict): Dictionary of visualization figures keyed by name
        theme (GameTheme): The game's theme object for styling

    Returns:
        list: List of Bootstrap tab components
    """
    return [
        dbc.Tab(
            dbc.Card(
                [dcc.Graph(figure=fig)],
                class_name="p-5",
                style={"backgroundColor": "inherit"},
            ),
            label=label,
            active_label_style={"backgroundColor": theme.secondary},
        )
        for label, fig in figures.items()
    ]


def create_leaderboard(leader_data: dict[str, int], theme: GameTheme) -> dbc.Table:
    """Create a styled leaderboard table.

    Args:
        leader_data (dict): Dictionary mapping player names to scores
        theme (GameTheme): The game's theme object for styling

    Returns:
        dbc.Table: Bootstrap table component displaying the leaderboard
    """
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


def create_statistics_card(fig: go.Figure, theme: GameTheme) -> dbc.Col:  # noqa: ARG001
    """Create a card displaying player performance statistics.

    Args:
        fig (go.Figure): Plotly figure with statistics visualization
        theme (GameTheme): The game's theme object for styling

    Returns:
        dbc.Col: Bootstrap column containing the statistics card
    """
    return dbc.CardBody(
        [
            dcc.Graph(
                figure=fig,
                style={"backgroundColor": "inherit"},
            ),
        ],
    )


def create_game_layout(app: Dash, theme: GameTheme) -> html.Div:
    """Create the main layout for the game application.

    This function builds the complete UI structure including the question display,
    answer options, timer, navigation controls, leaderboard, and statistics areas.

    Args:
        app (Dash): The Dash application instance
        theme (GameTheme): The game's theme object for styling

    Returns:
        html.Div: The main application layout
    """
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
                            ],
                        ),
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
                                            ),
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
                        ],
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


def init_callbacks(app: Dash, game_data: GameData, theme: GameTheme):  # noqa: ANN201
    """Initialize all the callback functions for the application.

    This function sets up the interactive behavior of the application by defining
    callbacks for timer updates, question navigation, modal interactions, and
    leaderboard/statistics updates.

    Args:
        app (Dash): The Dash application instance
        game_data (GameData): The game data instance
        theme (GameTheme): The game's theme object for styling
    """

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
    def update_timer(n_intervals, question_index):  # noqa: ANN001, ANN202, ARG001
        """Update the timer display and audio based on timer state.

        Args:
            n_intervals: Number of timer intervals elapsed
            question_index: Current question index (unused but required for callback)

        Returns:
            tuple: Timer display, audio loop state, audio source, time-up flag, interval count
        """
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
        if time_left == 30 and n_intervals != 0:  # noqa: PLR2004
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
    def update_question_and_options(current_index: int, time_up: bool):  # noqa: ANN202, FBT001
        """Update the displayed question and answer options.

        Args:
            current_index: Index of the current question
            time_up: Whether the timer has expired

        Returns:
            tuple: Question text, options grid
        """
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
    def navigate_questions(next_clicks: int, prev_clicks: int, current_index: int):  # noqa: ANN202, ARG001
        """Navigate between questions using the previous and next buttons.

        Args:
            next_clicks: Number of next button clicks
            prev_clicks: Number of previous button clicks
            current_index: Current question index

        Returns:
            int: Updated question index
        """
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
        [
            Output("modal-question", "is_open"),
            Output("modal-question-header", "children"),
            Output("visualization-tabs", "children"),
        ],
        Input("question-section", "n_clicks"),
        State("modal-question", "is_open"),
        State("current-question-index", "data"),
    )
    def toggle_question_modal(n_clicks: int, is_open: bool, curr_ques: int):  # noqa: ANN202, FBT001
        """Toggle the question visualization modal and update its content.

        Args:
            n_clicks: Number of clicks on the question section
            is_open: Current open state of the modal
            curr_ques: Current question index

        Returns:
            tuple: Modal open state, modal header content, tab content
        """
        if n_clicks:
            figs = qv.get_ques_vis(curr_ques)

            return not is_open, dbc.ModalTitle(game_data.questions[curr_ques]), create_modal_tabs(figs, theme)
        return is_open, no_update, no_update

    @app.callback(
        [
            Output("modal-answer", "is_open"),
            Output("visualisation-answer", "children"),
            Output("options-grid", "n_clicks"),
        ],
        [Input("options-grid", "n_clicks"), Input("time-up", "data")],
        State("modal-answer", "is_open"),
        State("current-question-index", "data"),
    )
    def toggle_answer_modal(n_clicks: int, time_up: bool, is_open: bool, curr_ques: int):  # noqa: ANN202, FBT001
        """Toggle the answer distribution modal and update its content.

        Args:
            n_clicks: Number of clicks on the options grid
            time_up: Whether the timer has expired
            is_open: Current open state of the modal
            curr_ques: Current question index

        Returns:
            tuple: Modal open state, modal content, reset click counter
        """
        if n_clicks and time_up:
            answer_data = game_data.answer_data
            # new_index = [chr(ord + 96).upper() for ord in answer_data["Answer"]]
            # answer_data["Answer"] = new_index
            fig = get_answer_distribution_graph(answer_data, curr_ques + 1)
            return not is_open, dcc.Graph(figure=fig), no_update
        return no_update, no_update, 0

    @app.callback(
        Output("leaderboard-card-body", "children"),
        Output("statistics-card", "children"),
        Input("time-up", "data"),
    )
    def update_leaderboard(time_up: bool):  # noqa: ANN202, FBT001
        """Update the leaderboard and statistics displays.

        Args:
            time_up: Whether the timer has expired

        Returns:
            tuple: Leaderboard content, statistics card content
        """
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


def run_app(debug: bool = False) -> None:  # noqa: FBT001, FBT002
    """Initialize and run the Dash application.

    This function creates the Dash app instance, initializes the game data and theme,
    sets up the layout and callbacks, and starts the server.

    Args:
        debug (bool, optional): Whether to run the app in debug mode. Defaults to False.
    """
    app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], assets_folder="assets")
    theme = GameTheme()
    game_data = GameData()

    app.layout = create_game_layout(app, theme)
    init_callbacks(app, game_data, theme)
    app.run_server(debug=debug)


if __name__ == "__main__":
    run_app(debug=True)
