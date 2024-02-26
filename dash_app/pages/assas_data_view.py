import dash
import dash_bootstrap_components as dbc
from dash import Dash, dash_table, html, dcc, Input, Output, callback, State
import pandas as pd
import numpy as np
from collections import OrderedDict
import h5py
import os

import logging

logger = logging.getLogger(__name__)

from assasdb import AssasDatabaseManager

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
    
    df = df.drop('system_uuid',axis=1)
    df = df.drop('system_path',axis=1)
    
    logger.info(df, type(df))
    print(df)
    
    return df
    
df = load_data()

ALL = len(df)
PAGE_SIZE = 30
PAGE_MAX_SIZE = 100

PAGE_COUNT = ALL / PAGE_SIZE

dash.register_page(__name__, path="/assas_data_view")

layout = html.Div([
    html.H2('ASSAS Database - ASTEC Dataset Index'),
    dbc.Alert("Search interface for the available ASTEC training datasets", color="primary", style={'textAlign': 'center'}),
    html.Div([
    dbc.Pagination(
                id='pagination', 
                first_last=True,
                previous_next=True,
                max_value=PAGE_COUNT, 
                fully_expanded=False,
                size="lg"                
                )
    ], style={'width': '100%','padding-left':'35%', 'padding-right':'25%'}),
    dash_table.DataTable(
        id='datatable-paging-and-sorting',
        columns=[
        {'name': '_id', 'id': '_id', 'hideable': True},
        {'name': 'Index', 'id': 'system_index', 'selectable': True},
        {'name': 'Size', 'id': 'system_size', 'selectable': True},
        {'name': 'Date', 'id': 'system_date', 'selectable': True},
        {'name': 'User', 'id': 'system_user', 'selectable': True},
        {'name': 'Download', 'id': 'system_download', 'selectable': True},
        {'name': 'Status', 'id': 'system_status', 'selectable': True},
        {'name': 'Name', 'id': 'meta_name', 'selectable': True},
        ],
        hidden_columns=['', '_id'],
        data=df.to_dict('records'),
        style_cell = {'textAlign': 'center'},
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
        
        style_data_conditional=[
                {'if': {'column_id': 'system_index'}, 'backgroundColor': 'green', 'text_align':'center','color': 'white'},
                {'if': {'column_id': 'system_download'}, 'backgroundColor': 'yellow', 'color': 'red', 'font-weight': 'bold'},
                {'if': {'column_id': 'meta_name'}, 'backgroundColor': 'yellow', 'color': 'blue', 'font-weight': 'bold'}
        ],        
    ),
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
        style={'color': 'grey'}
    ),
    html.Div('Select a page', id='pagination-contents'),             
    #html.Div('Or set the page dynamically using the slider below'),
    #dcc.Slider(
    #    id='page-change',
    #    min=1,
    #    max=len(df) + 1,
    #    step=1,
    #    value=1,
    #    marks={i: str(i) for i in range(1, 11)},
    #),   
])

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
    
    print("update page size", use_page_size, page_size_value, len(use_page_size))
    
    if len(use_page_size) == 0 or page_size_value is None:
        return PAGE_SIZE
    
    return page_size_value

@callback(
    Output('pagination-contents', 'children'),
    Input('pagination', 'active_page'),
    Input('pagination', 'max_value'))
def change_page(page, value):
    if page:
        return f'Page selected: {page}/{value}'
    return f'Page selected: 1/{value}'

@callback(
    Output('datatable-paging-and-sorting', 'page_current'),
    Input('pagination', 'active_page'))
def change_page_table(page):
    if page:
        return (page-1)
    return 0

@callback(
    Output('pagination', 'max_value'),
    Output('datatable-page-size', 'style'),
    Input('datatable-use-page-size', 'value'),
    Input('datatable-page-size', 'value'))
def update_page_count(use_page_size, page_size_value):
    
    print("use page size", use_page_size, page_size_value, len(use_page_size))
    
    if len(use_page_size) > 1 and page_size_value is not None:                
        return int(len(df) / page_size_value) + 1,{'color': 'black'}
    
    if page_size_value is None:
        int(len(df) / PAGE_SIZE) + 1,{'color': 'grey'}      
    
    return int(len(df) / PAGE_SIZE) + 1,{'color': 'grey'}

def generate_hdf5File():

    path = os.getcwd()+"/dataset.h5"
    
    file = h5py.File(path,"w")
    arr = np.random.randn(1000)
    file.create_group('metadata')
    file['metadata'].attrs['name'] = "lol"
    
    file.create_dataset("test", data=arr)
    file.close()
    
    return path 

@callback(
    Output('download', 'data'),
    Input('datatable-paging-and-sorting', 'active_cell'),
    State('datatable-paging-and-sorting', 'derived_viewport_data'))
def cell_clicked(active_cell, data):
    if active_cell:
        row = active_cell['row']
        col = active_cell['column_id']
        if col == 'system_download':
            #selected = data[row][col]
            path = generate_hdf5File()
            return dcc.send_file(path)
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
            print(str(active_cell), row_data['_id'], row_data['system_index'])
            url = '/details/' + str(row_data['_id'])
            return url
        else:
            return dash.no_update