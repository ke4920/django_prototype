
import dash
import dash_bootstrap_components as dbc
import logging

from dash import Dash, html, dcc
from flask import Flask, redirect
from flask_login import LoginManager, UserMixin
from logging.handlers import RotatingFileHandler

from users_mgt import User as base
from components import encode_svg_image

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('assas_app')
handler = RotatingFileHandler('assas_app.log', maxBytes=10000, backupCount=10)
logger.addHandler(handler)

logger = logging.getLogger('assas_app')

server = Flask(__name__)

logger.info("start application %s" % __name__)

@server.route('/')
def index_redirect():
    
    return redirect('/home')

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
                        dbc.Col(html.Img(src=encode_svg_image('kit_logo.drawio.svg'), height='60px', width='120px'), width=6),
                        dbc.Col(html.Img(src=encode_svg_image('assas_logo.svg'), height='60px', width='60px'), width=3),
                        dbc.Col(dbc.NavbarBrand("ASSAS Data Hub", className="ms-2"), width=3),                                           
                    ],
                    align="center",
                    className="g-0",
                ),
                #href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Home", href="/home", active="exact")),
                dbc.NavItem(dbc.NavLink("Database", href="/database", active="exact")),
                dbc.NavItem(dbc.NavLink("Upload", href="/upload", active="exact")),
                dbc.NavItem(dbc.NavLink("About", href="/about", active="exact")),
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

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# Create User class with UserMixin
class User(UserMixin, base):
    pass

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

logger.info("loaded application")

if __name__ == '__main__':
    
    app.server.logger.addHandler(handler)
    app.run(debug=True)