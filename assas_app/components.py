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
                "border":"3px grey solid",
            }

def conditional_table_style(): 

    return [
                {'if': {'column_id': 'system_index'}, 'backgroundColor': 'green', 'text_align':'center', 'color':'white'},
                {'if': {'column_id': 'system_download'}, 'backgroundColor': 'grey', 'textAlign':'center', 'textDecoration': 'underline', "cursor": "pointer", 'color': 'blue'},
                {'if': {'column_id': 'meta_name'}, 'backgroundColor': 'grey', 'color': 'blue', 'textAlign': 'center', 'textDecoration': 'underline', "cursor": "pointer", 'color': 'blue'}
        ]
    

