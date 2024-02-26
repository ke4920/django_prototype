import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, Dash

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

CONTENT_STYLE = {
    "color": "white",
}

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [                        
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
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

app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP], 
           use_pages=True, 
           suppress_callback_exceptions=True)

app.layout = html.Div([
                        navbar,  
                        html.Div([
                            html.Div(
                                dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
                                    ) for page in dash.page_registry.values()
                        ]),
                        dcc.Location(id="url"),
                        dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)