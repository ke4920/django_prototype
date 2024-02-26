import dash
from dash import html
import dash_bootstrap_components as dbc

from assasdb import AssasDatabaseManager

dash.register_page(__name__, path_template="/details/<report_id>")

def layout(report_id=None):
    
    print("%s" % (report_id))
    #database_manager = AssasDatabaseManager()
    #document = database_manager.get_file_document(report_id)
    #print("%s" % (document))
    
    table_header = [
        html.Thead(html.Tr([html.Th("Meta"), html.Th("Value")]))
    ]
    
    table_body = [
        html.Thead(html.Tr([html.Th("Meta"), html.Th("Value")]))
    ]

    #table_body2 = [html.Tbody([html.Tr([html.Td("Name"), html.Td(document["meta_name"])]),
    #                          html.Tr([html.Td("Group"), html.Td(document["meta_group"])]),
    #                          html.Tr([html.Td("Description"), html.Td(document["meta_description"])]),
    #                          html.Tr([html.Td("Variables"), html.Td(document["meta_description"])]),
    #                          html.Tr([html.Td("Channels"), html.Td(document["meta_description"])]),
    #                          html.Tr([html.Td("Meshes"), html.Td(document["meta_description"])]),
    #                          html.Tr([html.Td("Timesteps"), html.Td(document["meta_description"])])
    #                          ])
    #              ]
        
    return html.Div(        
        dbc.Table(table_header + table_body, bordered=True)
    )