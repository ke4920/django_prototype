from dash import Dash, dash_table, Input, Output, callback
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

PAGE_SIZE = 1

app.layout = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    page_size=20
)

#@callback(
#    Output('datatable-paging', 'data'),
#    Input('datatable-paging', "page_current"),
#    Input('datatable-paging', "page_size"))
#def update_table(page_current,page_size):
#    return df2.iloc[
#        page_current*page_size:(page_current+ 1)*page_size
#    ].to_dict('records')


if __name__ == '__main__':
    app.run(debug=True)