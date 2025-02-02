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

# Layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Who Wants to be a Millionaire?", 
                style={'color': '#FFD700', 'textAlign': 'center', 'marginBottom': '30px'})
    ], style={'padding': '20px'}),
    
    # Main content container
    dbc.Container([
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
], style={'backgroundColor': '#121212', 'minHeight': '100vh', 'padding': '20px'})

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