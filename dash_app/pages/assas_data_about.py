import dash
from dash import html

dash.register_page(__name__, path='/assas_data_about')

layout = html.Div([
    html.H1('This is our About page'),
    html.Div('This is our About page content.'),
])