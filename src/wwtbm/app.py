import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Initialize the Dash app with a dark theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Sample leaderboard data
leaderboard_data = [
    {"name": "John", "score": 500000},
    {"name": "Sarah", "score": 250000},
    {"name": "Mike", "score": 125000},
    {"name": "Emma", "score": 64000},
    {"name": "Alex", "score": 32000},
]

# Custom CSS for the hexagonal shapes
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .option-box {
                background-color: #000066;
                position: relative;
                color: white;
                padding: 15px 25px;
                margin: 10px 0;
                height: 60px;
                display: flex;
                align-items: center;
                clip-path: polygon(30px 0%, calc(100% - 30px) 0%, 100% 50%, calc(100% - 30px) 100%, 30px 100%, 0% 50%);
            }
            
            .option-box::after {
                content: '';
                position: absolute;
                top: 2px;
                left: 2px;
                right: 2px;
                bottom: 2px;
                background: inherit;
                clip-path: polygon(30px 0%, calc(100% - 30px) 0%, 100% 50%, calc(100% - 30px) 100%, 30px 100%, 0% 50%);
                z-index: 1;
            }
            
            .option-box::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: #4169E1;
                clip-path: polygon(30px 0%, calc(100% - 30px) 0%, 100% 50%, calc(100% - 30px) 100%, 30px 100%, 0% 50%);
            }
            
            .option-box:hover {
                background-color: #000099;
                cursor: pointer;
            }
            
            .question-box {
                background-color: #000066;
                position: relative;
                color: white;
                padding: 20px 30px;
                margin: 20px 0;
                min-height: 80px;
                display: flex;
                align-items: center;
                justify-content: center;
                clip-path: polygon(40px 0%, calc(100% - 40px) 0%, 100% 50%, calc(100% - 40px) 100%, 40px 100%, 0% 50%);
            }
            
            .question-box::after {
                content: '';
                position: absolute;
                top: 2px;
                left: 2px;
                right: 2px;
                bottom: 2px;
                background: inherit;
                clip-path: polygon(40px 0%, calc(100% - 40px) 0%, 100% 50%, calc(100% - 40px) 100%, 40px 100%, 0% 50%);
                z-index: 1;
            }
            
            .question-box::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: #4169E1;
                clip-path: polygon(40px 0%, calc(100% - 40px) 0%, 100% 50%, calc(100% - 40px) 100%, 40px 100%, 0% 50%);
            }

            /* Ensure text appears above the pseudo-elements */
            .option-box span, .question-box span {
                position: relative;
                z-index: 2;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Who Wants to be a Millionaire?", 
                style={'color': '#FFD700', 'textAlign': 'center', 'marginBottom': '30px'})
    ], style={'padding': '20px'}),
    
    # Main content container
    dbc.Container([
        # Question Section
        dbc.Row([
            dbc.Col([
                html.Div([
                    # Question
                    html.Div(
                        html.Span("What is the capital city of France?"),
                        className='question-box',
                        style={'fontSize': '24px', 'textAlign': 'center'}
                    ),
                    
                    # Options container
                    html.Div([
                        dbc.Row([
                            dbc.Col(
                                html.Div(html.Span("A: Paris"), className='option-box'),
                                width=6
                            ),
                            dbc.Col(
                                html.Div(html.Span("B: London"), className='option-box'),
                                width=6
                            ),
                        ]),
                        dbc.Row([
                            dbc.Col(
                                html.Div(html.Span("C: Berlin"), className='option-box'),
                                width=6
                            ),
                            dbc.Col(
                                html.Div(html.Span("D: Madrid"), className='option-box'),
                                width=6
                            ),
                        ]),
                    ], style={'marginTop': '20px'})
                ], style={'marginBottom': '30px'})
            ], width=12)
        ]),
        
        dbc.Row([
            # Timer and Leaderboard Column
            dbc.Col([
                # Timer Card
                dbc.Card([
                    dbc.CardHeader("Timer", style={'backgroundColor': '#1a1a1a', 'color': '#FFD700'}),
                    dbc.CardBody([
                        html.H2(id='timer-display', children='30',
                               style={'color': '#FFD700', 'textAlign': 'center', 'fontSize': '48px'})
                    ], style={'backgroundColor': '#2a2a2a'})
                ], className='mb-4'),
                
                # Leaderboard Card
                dbc.Card([
                    dbc.CardHeader("Leaderboard", style={'backgroundColor': '#1a1a1a', 'color': '#FFD700'}),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.H5(f"{entry['name']}", style={'display': 'inline-block', 'marginRight': '10px'}),
                                html.Span(f"${entry['score']:,}", style={'color': '#FFD700'})
                            ], className='mb-2') for entry in leaderboard_data
                        ], style={'backgroundColor': '#2a2a2a'})
                    ], style={'backgroundColor': '#2a2a2a'})
                ])
            ], width=4),
            
            # Visualization Section
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Question Statistics", style={'backgroundColor': '#1a1a1a', 'color': '#FFD700'}),
                    dbc.CardBody([
                        html.Div(id='visualization-container', children=[
                            html.H4("Visualization Area", style={'color': '#FFD700', 'textAlign': 'center'}),
                            html.P("Statistical visualizations for current question will appear here.",
                                 style={'color': '#ffffff', 'textAlign': 'center'})
                        ], style={'height': '400px', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'})
                    ], style={'backgroundColor': '#2a2a2a'})
                ], style={'height': '100%'})
            ], width=8)
        ])
    ], fluid=True)
], style={'backgroundColor': '#00003B', 'minHeight': '100vh', 'padding': '20px'})

# Timer callback
@app.callback(
    Output('timer-display', 'children'),
    Input('timer-display', 'id')
)
def update_timer(value):
    # In a real application, you would implement proper timer logic here
    return "30"

if __name__ == '__main__':
    app.run_server(debug=True)
