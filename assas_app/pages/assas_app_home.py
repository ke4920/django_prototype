import dash

from dash import html
from components import content_style, encode_svg_image

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('ASSAS Database'),
    html.H2('ASSAS Data Hub'),
    html.H5('A software platform to store and visualize training datasets for ASTEC simulations.'),
    ],
    style=content_style()
)