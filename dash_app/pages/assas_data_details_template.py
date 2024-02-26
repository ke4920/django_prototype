import dash
from dash import html
import dash_bootstrap_components as dbc

from assasdb import AssasDatabaseManager

dash.register_page(__name__, path_template="/details/<report_id>")

def meta_info_table(document):
    
    general_header = [
            html.Thead(html.Tr([html.Th("General")]))
        ]
    
    general_body = [html.Tbody([html.Tr([html.Td("Name"), html.Td(document["meta_name"])]),
                                html.Tr([html.Td("Group"), html.Td(document["meta_group"])]),
                                html.Tr([html.Td("Description"), html.Td(document["meta_description"])])
                            ])]
    
    data_header = [
            html.Thead(html.Tr([html.Th("Data")]))
        ]
    
    data_body = [html.Tbody([html.Tr([html.Td("Variables"), html.Td(document["meta_data_variables"])]),
                             html.Tr([html.Td("Channels"), html.Td(document["meta_data_channels"])]),
                             html.Tr([html.Td("Meshes"), html.Td(document["meta_data_meshes"])]),
                             html.Tr([html.Td("Timesteps"), html.Td(document["meta_data_timesteps"])])
                            ])]
    
    table = general_header + general_body + data_header + data_body
    
    return dbc.Table(table, striped=True, bordered=True, hover=True, responsive=True)

def layout(report_id=None):
    
    print("report_id %s" % (report_id))
    
    if report_id == 'none':
        return html.Div([
            html.H1('This is the data details template.'),
            html.Div('The content is generated for each _id.'),
            ])
    else:
        database_manager = AssasDatabaseManager()
        document = database_manager.get_file_document(report_id)
        print("document %s" % (document))
    
        return html.Div([    
            meta_info_table(document)            
        ])