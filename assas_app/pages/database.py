import dash
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import logging

from dash import Dash, dash_table, html, dcc, Input, Output, callback, State

from assasdb import AssasDatabaseManager
from components import content_style, conditional_table_style

logger = logging.getLogger('assas_app')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def load_data():
    
    df = AssasDatabaseManager().view()    
    df['system_index'] = range(1, len(df) + 1)    
    df['_id'] = df['_id'].astype(str)    
   
    return df
    
df = load_data()

ALL = len(df)
PAGE_SIZE = 30
PAGE_MAX_SIZE = 100

PAGE_COUNT = ALL / PAGE_SIZE

dash.register_page(__name__, path="/database")

layout = html.Div([
    html.H2('ASSAS Database - Training Dataset Index'),
    dbc.Alert("Search interface for the available ASSAS training datasets", color="primary", style={'textAlign': 'center'}),
    html.Hr(),
    html.Div([
    dbc.Pagination(
                id='pagination', 
                first_last=True,
                previous_next=True,
                max_value=PAGE_COUNT, 
                fully_expanded=False,
                size="lg"                
                )
    ], style={'width': '100%','padding-left':'30%', 'padding-right':'25%'}),
    html.Hr(),
    html.Div([
    dbc.Button(
            "Download", 
            id="download_selected", 
            className="me-2", 
            n_clicks=0, 
            disabled=True,
        ),
    dbc.Button(
            "Reload", 
            id="reload_page", 
            className="me-2", 
            n_clicks=0, 
            disabled=True,
        ),
    ], style={'width': '100%','padding-left':'10%', 'padding-right':'25%'}),
    html.Hr(),
    dash_table.DataTable(
        id='datatable-paging-and-sorting',
        columns=[
        {'name': '_id', 'id': '_id', 'hideable': True},
        {'name': 'uuid', 'id': 'system_uuid', 'hideable': True},
        {'name': 'Path', 'id': 'system_path', 'hideable': True},
        {'name': 'Index', 'id': 'system_index', 'selectable': True},
        {'name': 'Size', 'id': 'system_size', 'selectable': True},
        {'name': 'Date', 'id': 'system_date', 'selectable': True},
        {'name': 'User', 'id': 'system_user', 'selectable': True},
        {'name': 'File', 'id': 'system_download', 'selectable': True},
        {'name': 'Status', 'id': 'system_status', 'selectable': True},
        {'name': 'Name', 'id': 'meta_name', 'selectable': True},
        ],
        markdown_options={"html": True},
        hidden_columns=['', '_id', 'system_uuid', 'system_path'],
        data=df.to_dict('records'),
        style_cell={
            'fontSize': 17,
            'padding': '2px',
            'textAlign': 'center'
        },
        merge_duplicate_headers= True,        
        
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_data={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        },
        
        row_selectable='multi',
        
        page_current=0,
        page_size=PAGE_SIZE,
        page_action='none',
                
        filter_action='custom',
        filter_query='',

        sort_action='custom',
        sort_mode='multi',
        sort_by=[],
        
        is_focused=True,
        
        style_data_conditional=conditional_table_style(),        
    ),
    html.Hr(),
    dcc.Location(id='location'),
    dcc.Download(id='download'),
    html.Br(),
    dcc.Checklist(
        id='datatable-use-page-size',
        options=[
            {'label': ' Change entries per page', 'value': 'True'}
        ],
        value=['False']
    ),
    'Entries per page: ',
    dcc.Input(
        id='datatable-page-size',
        type='number',
        min=1,
        max=PAGE_MAX_SIZE,
        value=PAGE_SIZE,
        placeholder=PAGE_SIZE,
        style={'color': 'grey'},
        disabled=False,
    ),
    html.Div('Select a page', id='pagination-contents'),    
],style=content_style())

@callback(
    Output("download_selected", "disabled"),     
    Input("datatable-paging-and-sorting", "derived_viewport_selected_rows"),
    Input("datatable-paging-and-sorting", "derived_viewport_selected_row_ids")
)
def selected_button(rows, ids):
    
    if (rows is None) or (ids is None):                                                                                                                                                                                                                      
        return dash.no_update
        
    if len(rows) > 0:
        return False
    
    return True

@callback(
    Output("datatable-paging-and-sorting", "style_data_conditional"),
    Input("datatable-paging-and-sorting", "derived_viewport_selected_rows"),
    Input("datatable-paging-and-sorting", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selected_rows, selected_row_ids):
    
    if selected_rows is None:                                                                                                                                                                                                                      
        return dash.no_update
    
    logger.debug('%s %s ' % (selected_rows, selected_row_ids))
    
    val = [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "green",}
        for i in selected_rows        
    ]   
    
    val2 = conditional_table_style()
    
    return val + val2

def split_filter_part(filter_part):
    
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in (''', ''', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

@callback(
    Output('datatable-paging-and-sorting', 'data'),
    Input('datatable-paging-and-sorting', 'page_current'),
    Input('datatable-paging-and-sorting', 'page_size'),
    Input('datatable-paging-and-sorting', 'sort_by'),
    Input('datatable-paging-and-sorting', 'filter_query'))
def update_table(page_current, page_size, sort_by, filter):
    
    filtering_expressions = filter.split(' && ')
    
    dff = df
    
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    page = page_current
    size = page_size
    
    return dff.iloc[page * size: (page + 1) * size].to_dict('records')

@callback(
    Output('datatable-paging-and-sorting', 'page_size'),
    Input('datatable-use-page-size', 'value'),
    Input('datatable-page-size', 'value'))
def update_page_size(use_page_size, page_size_value):
    
    logger.debug('update page size, use page size %s page size value %s' % (str(use_page_size), str(page_size_value)))
    
    if len(use_page_size) == 0 or page_size_value is None:
        return PAGE_SIZE
    
    return page_size_value

@callback(
    Output('pagination-contents', 'children'),
    Input('pagination', 'active_page'),
    Input('pagination', 'max_value'))
def change_page(page, value):
    
    logger.debug('page %s value %s' % (str(page), str(value)))
    
    if page:
        
        return f'Page selected: {page}/{value}'
    
    return f'Page selected: 1/{value}'

@callback(
    Output('datatable-paging-and-sorting', 'page_current'),
    Input('pagination', 'active_page'))
def change_page_table(page):
    
    logger.debug('page %s' % (str(page)))
    
    if page:
        
        return (page - 1)
    
    return 0

@callback(
    Output('pagination', 'max_value'),
    Output('datatable-page-size', 'style'),
    Input('datatable-use-page-size', 'value'),
    Input('datatable-page-size', 'value'))
def update_page_count(use_page_size, page_size_value):
    
    logger.debug('update page count, use page size %s page size value %s' % (str(use_page_size), str(page_size_value)))
    
    if len(use_page_size) > 1 and page_size_value is not None:                
        return int(len(df) / page_size_value) + 1,{'color': 'black'}
    
    if page_size_value is None:
        return int(len(df) / PAGE_SIZE) + 1,{'color': 'grey'}      
    
    return int(len(df) / PAGE_SIZE) + 1,{'color': 'grey'}

@callback(
    Output('download', 'data'),
    Input('datatable-paging-and-sorting', 'active_cell'),
    State('datatable-paging-and-sorting', 'derived_viewport_data'))
def cell_clicked_download(active_cell, data):
    
    if active_cell:
        
        row = active_cell['row']
        row_data = data[row]
        col = active_cell['column_id']
        
        if col == 'system_download':
            
            logger.info('start download for %s' % row_data['system_path'])
            
            return dcc.send_file(row_data['system_path']+'/dataset.h5')
        
        else:
            
            return dash.no_update
        
@callback(
    Output('location', 'href'),
    Input('datatable-paging-and-sorting', 'active_cell'),
    State('datatable-paging-and-sorting', 'derived_viewport_data'))
def cell_clicked_details(active_cell, data):
    
    if active_cell:
        
        row = active_cell['row']
        row_data = data[row]
        col = active_cell['column_id']
        
        if col == 'meta_name':
            url = '/details/' + str(row_data['_id'])
            return url
        else:
            return dash.no_update