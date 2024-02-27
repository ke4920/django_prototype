import dash
import dash_bootstrap_components as dbc
import logging

from dash import dcc, html, Dash
from flask import Flask
from components import encode_svg_image
from logging.handlers import RotatingFileHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('assas_app')
handler = RotatingFileHandler('assas_app.log', maxBytes=10000, backupCount=1)
logger.addHandler(handler)

server = Flask(__name__)

logger.info("start application")

app = Dash(__name__,
           server = server,
           assets_folder='/assets',
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           use_pages=True, 
           suppress_callback_exceptions=True)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [                        
                        dbc.Col(html.Img(src=encode_svg_image('assas_logo.svg'), height='30px')),
                        dbc.Col(dbc.NavbarBrand("ASSAS Data Hub", className="ms-2")),                                           
                    ],
                    align="center",
                    className="g-0",
                ),
                #href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Home", href="/", active="exact")),
                dbc.NavItem(dbc.NavLink("Database", href="/assas_data_view", active="exact")),
                dbc.NavItem(dbc.NavLink("Upload", href="/assas_data_upload", active="exact")),
                dbc.NavItem(dbc.NavLink("About", href="/assas_data_about", active="exact")),
            ],
            vertical=False,
            pills=True,
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),            
        ]
    ),    
    color="dark",
    dark=True,    
)

app.layout = html.Div(
                [
                    navbar,  
                    #html.Div([
                    #    html.Div(
                    #        dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
                    #            ) for page in dash.page_registry.values()
                    #]),
                    dcc.Location(id="url"),
                    dash.page_container
                ])

logger.info("started application")

if __name__ == '__main__':
    app.server.logger.addHandler(handler)
    app.run(debug=True)