import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import dcc, html

def create_navbar():
    navbar = dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col([
                            html.Div([
                                html.Img(src="https://i.pinimg.com/originals/4c/78/65/4c78654be43dc14f7509346806361a68.png", height="45px", style={'margin-left': '20px'})
                            ], style={'display': 'flex', 'alignItems': 'center'}),
                        ], className="mr-3 text-center")
                    ],
                    align="center",
                ),
            )
        ],
        color="dark",
        dark=True,
    )
    return navbar

def create_home_layout(df):
    layout = html.Div([
        create_navbar(),
        dbc.Row([
            dbc.Col([
                html.Div(style={'backgroundColor': '#1E1E1E', 'color': '#FFFFFF', 'margin': '20px'}, children=[
                    html.Div([
                        html.Div([
                            html.H4("Welcome to the Campus Watch Dashboard, New Brunswick", style={'color': 'white'}),
                            html.Label("Explore crime incidents reported on campus, filter by crime type, status, and date range, and visualize crime density on the map. Stay informed and stay safe!", style={'color': 'white'})
                        ],style={'margin': '10px'}),

                        html.Div([
                            html.Label("Crime Type", style={'font-weight': 'bold', 'color': '#FFFFFF','margin-bottom':'7px'}),
                            dcc.Dropdown(
                                id='crime-type-dropdown',
                                options=[{'label': crime_type, 'value': crime_type} for crime_type in df['Nature'].unique()],
                                value=None,
                                multi=True,  # Make the dropdown multi-select
                                clearable=True,
                                style={'width': '100%', 'backgroundColor': '#343A40', 'color': '#1E1E1E',
                                    'border': '1px solid #6C757D', 'border-radius': '5px', 'box-shadow': 'none'},
                            ),
                        ],style={'margin': '10px'}),
                        html.Div([
                            html.Label("Status", style={'font-weight': 'bold', 'color': '#FFFFFF','margin-bottom':'7px'}),
                            dbc.RadioItems(
                                id='status-radio',
                                options=[
                                    {'label': 'All', 'value': 'All'},
                                    {'label': 'Open/Pending', 'value': 'Open/Pending'},
                                    {'label': 'Closed', 'value': 'Closed'},
                                ],
                                value='All',
                                inline=True,
                                labelStyle={'margin-right': '15px', 'color': '#FFFFFF'}
                            ),
                        ],style={'margin': '10px'}),
                        html.Div([
                            html.Label("Select Date Range", style={'font-weight': 'bold', 'color': '#FFFFFF','margin-bottom': '10px'}),
                            dcc.DatePickerRange(
                                id='date-picker',
                                start_date=df['Report Date'].min(),
                                end_date=df['Report Date'].max(),
                                display_format='MM-DD-YYYY',
                                style={'width': '100%', 'color': '#FFFFFF', 'border': 'none', 'box-shadow': 'none', 'margin-bottom': '10px'}
                            )
                        ],style={'margin': '10px'}),
                    ]),
                ]),
                html.Div(id='area-wise-crimes', style={'margin': '20px'}),
            ], width=12, lg=3),  # Adjust width for large screens
            dbc.Col([
                html.Div([
                    dcc.Graph(id='density-map', config={'scrollZoom': True}, style={'margin': '20px 0', 'backgroundColor': '#1E1E1E', 'height': '400px'}),
                    dcc.Graph(id='top-crimes-chart', style={'margin': '20px 0', 'height': '400px'})
                ]),
            ], width=12, lg=9),  # Adjust width for large screens
        ]),
    ], style={'max-width': '100vw', 'overflow-x': 'hidden'})  # Adjust max width and overflow
    return layout