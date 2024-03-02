import dash

from dash import html
from components import content_style, encode_svg_image

dash.register_page(__name__, path='/about')

layout = html.Div([
    html.H1('About this Project'),
    html.Hr(),
    html.H4('System Overview'),
    html.Hr(),
    html.Img(src=encode_svg_image('assas_data_hub_system.drawio.svg'), height='600px', width='900px'),
    html.Hr(),
    html.H4('Data Flow'),
    html.Hr(),
    html.Img(src=encode_svg_image('assas_data_flow.drawio.svg'), height='600px', width='900px'),
    ],
    style = content_style()
)