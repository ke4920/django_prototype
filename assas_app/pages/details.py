import dash

from dash import html
from components import content_style

dash.register_page(__name__, path='/details')

layout = html.Div([
    html.H1('This is our Details page'),
    html.Div('This is our Details page content.'),
    ],
    style=content_style()
)