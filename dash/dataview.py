from dash import Dash, dash_table, html, dcc, Input, Output, callback
import pandas as pd
import numpy as np
from collections import OrderedDict

from assasdb import AssasDatabaseManager

df = AssasDatabaseManager().view()
df['index'] = range(1, len(df) + 1)
df = df.drop("_id",axis=1)
df = df.drop("path",axis=1)
df = df.drop("uuid",axis=1)

print(df, type(df))

app = Dash(__name__)

PAGE_SIZE = 10

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-paging-and-sorting',
        columns=[
            {'name': i, 'id': i, 'deletable': True} for i in sorted(df.columns)
        ],
        page_current=0,
        page_size=PAGE_SIZE,
        page_action='custom',

        sort_action='custom',
        sort_mode='single',
        sort_by=[]
    ),
    html.Br(),
    #dcc.Checklist(
    #    id='datatable-use-page-count',
    #    options=[
    #        {'label': 'Use page_count', 'value': 'True'}
    #    ],
    #    value=['True']
    #),
    'Page count: ',
    dcc.Input(
        id='datatable-page-count',
        type='number',
        min=1,
        max=29,
        value=10
    )
])

@callback(
    Output('datatable-paging-and-sorting', 'page_count'),
    Input('datatable-page-count', 'value'))
def update_table(page_count_value):
    if page_count_value is None:
        return None
    return page_count_value

@callback(
    Output('datatable-paging-and-sorting', 'data'),
    Input('datatable-paging-and-sorting', 'page_current'),
    Input('datatable-paging-and-sorting', 'page_size'),
    Input('datatable-paging-and-sorting', 'sort_by'))
def update_table(page_current, page_size, sort_by):
    if len(sort_by):
        dff = df.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = df

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

if __name__ == '__main__':
    app.run(debug=True, port=8051)