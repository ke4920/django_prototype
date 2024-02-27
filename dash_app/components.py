import dash
import os
import base64
from dash import html

def encode_svg_image(svg_name):
    
    logo = os.getcwd() + dash.get_asset_url(svg_name)
    encoded = base64.b64encode(open(logo,'rb').read())
    svg = 'data:image/svg+xml;base64,{}'.format(encoded.decode())
    
    return svg

