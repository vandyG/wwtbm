import base64

import dash_bootstrap_components as dbc
from dash import Dash, html

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], assets_folder="assets")


def create_game_layout():
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
                            html.Div(
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
                                        style={"marginTop": "20px", "fontSize": "24px"},
                                    ),
                                ],
                            ),
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
                ],
                fluid=True,
            ),
        ],
        style={"backgroundColor": "#00003B", "minHeight": "100vh", "padding": "20px"},
    )


app.layout = create_game_layout()

if __name__ == "__main__":
    app.run_server(debug=True)
