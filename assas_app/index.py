import dash
import logging 

import dash_bootstrap_components as dbc

from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from flask_login import logout_user, current_user
from logging.handlers import RotatingFileHandler

from app import app, server
from pages import login, error, database, upload, home, profile, user_admin
from components import encode_svg_image

navBar = dbc.Navbar(id='navBar',
    children=[],
    sticky='top',
    color='primary',
    className='navbar navbar-expand-lg navbar-dark bg-primary',
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        navBar,
        html.Div(id='pageContent')
    ])
], id='table-wrapper')


################################################################################
# HANDLE PAGE ROUTING - IF USER NOT LOGGED IN, ALWAYS RETURN TO LOGIN SCREEN
################################################################################
@app.callback(Output('pageContent', 'children'),
              [Input('url', 'pathname')])
def displayPage(pathname):
    if pathname == '/':
        if current_user.is_authenticated:
            return home.layout
        else:
            return login.layout

    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return login.layout
        else:
            return login.layout

    if pathname == '/database':
        if current_user.is_authenticated:
            return database.layout
        else:
            return login.layout

    if pathname == '/upload':
        if current_user.is_authenticated:
            return upload.layout
        else:
            return login.layout

    if pathname == '/profile':
        if current_user.is_authenticated:
            return profile.layout
        else:
            return login.layout

    if pathname == '/admin':
        if current_user.is_authenticated:
            if current_user.admin == 1:
                return user_admin.layout
            else:
                return error.layout
        else:
            return login.layout


    else:
        return error.layout


################################################################################
# ONLY SHOW NAVIGATION BAR WHEN A USER IS LOGGED IN
################################################################################
@app.callback(
    Output('navBar', 'children'),
    [Input('pageContent', 'children')])
def navBar(input1):
    if current_user.is_authenticated:
        if current_user.admin == 1:
            navBarContents = [
                dbc.NavItem(dbc.NavLink('Database', href='/database')),
                dbc.NavItem(dbc.NavLink('Upload', href='/upload')),
                dbc.DropdownMenu(
                    nav=True,
                    in_navbar=True,
                    label=current_user.username,
                    children=[
                        dbc.DropdownMenuItem('Profile', href='/profile'),
                        dbc.DropdownMenuItem('Admin', href='/admin'),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem('Logout', href='/logout'),
                    ],
                ),
            ]
            return navBarContents

        else:
            navBarContents = [
                dbc.NavItem(dbc.NavLink('Database', href='/database')),
                dbc.NavItem(dbc.NavLink('Upload', href='/upload')),
                dbc.DropdownMenu(
                    nav=True,
                    in_navbar=True,
                    label=current_user.username,
                    children=[
                        dbc.DropdownMenuItem('Profile', href='/profile'),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem('Logout', href='/logout'),
                    ],
                ),
            ]
            return navBarContents

    else:
        return ''
