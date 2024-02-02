import dash
import dash_bootstrap_components as dbc
from dash import Dash, dash_table, html, dcc, Input, Output, callback, State
import pandas as pd
import numpy as np
from collections import OrderedDict

import logging

logger = logging.getLogger(__name__)

from assasdb import AssasDatabaseManager

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

def load_data():
    
    df = AssasDatabaseManager().view()
    df['index'] = range(1, len(df) + 1)
    df = df.drop('_id',axis=1)
    df = df.drop('file_path',axis=1)
    df = df.drop('uuid',axis=1)
    #df = df.drop('common_description',axis=1)
    
    logger.info(df, type(df))
    
    return df
    
df = load_data()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

ALL = len(df)
PAGE_SIZE = 30
PAGE_MAX_SIZE = 100

PAGE_COUNT = ALL / PAGE_SIZE

app.layout = html.Div([
    html.H2('ASSAS Database - ASTEC Dataset Index'),
    dbc.Alert("This is a primary alert", color="primary"),
    dbc.Pagination(
                id='pagination', 
                first_last=True,
                previous_next=True,
                max_value=PAGE_COUNT, 
                fully_expanded=False,
                size="lg"
                ),
    dash_table.DataTable(
        id='datatable-paging-and-sorting',
        columns=[
        {'name': ['', 'Index'], 'id': 'index'},
        {'name': ['File', 'Name'], 'id': 'file_name'},
        {'name': ['File', 'Size'], 'id': 'file_size'},
        {'name': ['File', 'Date'], 'id': 'file_date'},
        {'name': ['File', 'User'], 'id': 'file_user'},
        {'name': ['File', 'Download'], 'id': 'file_download'},
        {'name': ['Common', 'Scenario'], 'id': 'common_scenario'},
        {'name': ['Common', 'Description'], 'id': 'common_description'},
        {'name': ['Common', 'Attribute 1'], 'id': 'common_attribute_1'},
        {'name': ['Common', 'Attribute 2'], 'id': 'common_attribute_2'},
        {'name': ['Common', 'Attribute 3'], 'id': 'common_attribute_3'},
        {'name': ['Data', 'Variables'], 'id': 'data_variables'},
        {'name': ['Data', 'Channels'], 'id': 'data_channels'},
        {'name': ['Data', 'Meshes'], 'id': 'data_meshes'},
        {'name': ['Data', 'Timesteps'], 'id': 'data_timesteps'},
        ],
        data=df.to_dict('records'),
        style_cell = {'textAlign': 'center'},
        merge_duplicate_headers= True,        
        
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white'
        },
        style_data={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        },
        
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
                {'if': {'column_id': 'index'}, 'backgroundColor': 'green', 'text_align':'center','color': 'white'},
                {'if': {'column_id': 'file_download'}, 'backgroundColor': 'yellow', 'color': 'red', 'font-weight': 'bold'},
        ],        
    ),
    dcc.Location(id='location'),
    dcc.Download(id='download'),
    html.Br(),
    dcc.Checklist(
        id='datatable-use-page-size',
        options=[
            {'label': 'Change number of entries per page', 'value': 'True'}
        ],
        value=['True']
    ),
    'Entries per page: ',
    dcc.Input(
        id='datatable-page-size',
        type='number',
        min=1,
        max=PAGE_MAX_SIZE,
        value=PAGE_SIZE,
        placeholder=PAGE_SIZE,
        style={'color': 'black'}
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

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

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
    if use_page_size:
        logger.info("use page size %d %d", len(df), page_size_value)
        return int(len(df) / page_size_value)+1,{'color': 'black'}
    logger.info("not use page size %d %d", len(df), page_size_value)
    return int(len(df) / PAGE_SIZE)+1,{'color': 'grey'}

@callback(
    Output('download', 'data'),
    Input('datatable-paging-and-sorting', 'active_cell'),
    State('datatable-paging-and-sorting', 'derived_viewport_data'))
def cell_clicked(active_cell, data):
    if active_cell:
        row = active_cell['row']
        col = active_cell['column_id']

        if col == 'index':  # or whatever column you want
            selected = data[row][col]
            return dict(content='Hello!', filename='hello.txt')
        else:
            return dash.no_update

if __name__ == '__main__':
    app.run(debug=True, port=8051)