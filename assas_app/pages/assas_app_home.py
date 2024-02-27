import dash

from dash import html
from components import content_style

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('This is our Home page'),
    html.Div('This is our Home page content.'),
    ],
    style=content_style()
)