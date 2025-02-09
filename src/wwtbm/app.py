import base64

import dash_bootstrap_components as dbc
from dash import Dash, html

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], assets_folder="assets")

# Simplified CSS with consistent styling
CUSTOM_STYLES = """
.hex-shape {
    background-color: #000066;
    position: relative;
    color: white;
    display: flex;
    align-items: center;
    clip-path: polygon(30px 0%, calc(100% - 30px) 0%, 100% 50%, calc(100% - 30px) 100%, 30px 100%, 0% 50%);
}

.hex-shape::after {
    content: '';
    position: absolute;
    inset: 2px;
    background: inherit;
    clip-path: polygon(30px 0%, calc(100% - 30px) 0%, 100% 50%, calc(100% - 30px) 100%, 30px 100%, 0% 50%);
    z-index: 1;
}

.hex-shape::before {
    content: '';
    position: absolute;
    inset: 0;
    background: #4169E1;
    clip-path: polygon(30px 0%, calc(100% - 30px) 0%, 100% 50%, calc(100% - 30px) 100%, 30px 100%, 0% 50%);
}

.hex-shape:hover {
    background-color: #000099;
    cursor: pointer;
}

.hex-shape span {
    position: relative;
    z-index: 2;
    font-size: 18px;
}

.option-box { 
    padding: 15px 25px;
    height: 60px;
    margin: 10px 0;
}

.question-box {
    padding: 20px 30px;
    min-height: 80px;
    margin: 20px 0;
    justify-content: center;
}

.hex-button {
    width: 250px;
    height: 60px;
    border: none;
    padding: 0;
    margin: 10px;
    justify-content: center;
}

.hex-button span {
    font-weight: 500;
}
"""


def create_game_layout(image_path):
    encoded_image = base64.b64encode(open(image_path, "rb").read()).decode()

    return html.Div(
        [
            # Logo
            html.Div(
                html.Img(src=f"data:image/svg;base64,{encoded_image}", style={"height": "20%", "width": "20%"}),
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
                                        className="hex-shape question-box",
                                        style={"fontSize": "24px", "textAlign": "center"},
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
                                        style={"marginTop": "20px"},
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
                                dbc.Card(
                                    [
                                        html.Div(html.Span("Timer"), className="hex-shape question-box mb-0"),
                                        dbc.CardBody(
                                            html.H2(
                                                "30",
                                                id="timer-display",
                                                style={"color": "#FFD700", "textAlign": "center", "fontSize": "48px"},
                                            ),
                                        ),
                                    ],
                                    style={"backgroundColor": "#00003B"},
                                ),
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
                                    style={
                                        "display": "flex",
                                        "justifyContent": "center",
                                        "gap": "20px",
                                        "marginTop": "20px",
                                    },
                                ),
                            ),
                        ],
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
                        # width=8,
                    ),
                ],
                fluid=True,
            ),
        ],
        style={"backgroundColor": "#00003B", "minHeight": "100vh", "padding": "20px"},
    )


app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>{CUSTOM_STYLES}</style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

app.layout = create_game_layout("/home/vandy/work/datavis/wwtbm/src/assets/WWTBAMUS2020Logo.webp")

if __name__ == "__main__":
    app.run_server(debug=True)
