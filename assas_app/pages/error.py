
import dash_bootstrap_components as dbc

from dash import html, dcc

from components import encode_svg_image

layout = dbc.Container([
    html.Br(),
    dbc.Container([
        dcc.Location(id='err404', refresh=True),
        dbc.Container(
            html.Img(
                src=encode_svg_image('assas_logo.svg'),
                className='center'
            ),
        ),
        dbc.Container([
            dbc.Container(id='outputState', children='Error 404 - Page not found')
        ], className='form-group'),
    ], className='jumbotron')
])
