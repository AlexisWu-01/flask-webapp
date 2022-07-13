"""Instantiate a Dash app."""
import dash
from dash import html

from .data import create_dataframe
from .layout import html_layout


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[
            "https://fonts.googleapis.com/css?family=Lato"
        ],
    )

    # Load DataFrame
    df = create_dataframe()

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(
        children=[
            html.H1(children="Hello World!")
        ],
        id="dash-container",
    )
    return dash_app.server