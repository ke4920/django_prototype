import dash

from dash import html
from components import content_style

dash.register_page(__name__, path='/assas_data_about')

layout = html.Div([
    html.H1('This is our About page'),
    html.Div('This is our About page content.'),
    ],
    style = content_style()
)