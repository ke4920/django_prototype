import dash
import os
import base64

def encode_svg_image(svg_name):
    
    logo = os.getcwd() + dash.get_asset_url(svg_name)
    encoded = base64.b64encode(open(logo,'rb').read())
    svg = 'data:image/svg+xml;base64,{}'.format(encoded.decode())
    
    return svg

def content_style():
    
    return {
                "margin-top": "1rem",
                "margin-bottom": "1rem",
                "margin-left": "1rem",
                "margin-right": "1rem",
                "padding": "2rem 1rem",
                "border":"6px grey solid",
            }
    
    

