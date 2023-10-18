from dash import Dash, dash_table, Input, Output, callback
import pandas as pd

from assasdb import DatabaseManager

df = DatabaseManager().view()
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

df[' index'] = range(1, len(df) + 1)

app = Dash(__name__)

PAGE_SIZE = 10

app.layout = dash_table.DataTable(
    id='datatable-paging',
    columns=[
        {"name": i, "uuid": i} for i in sorted(df.columns)
    ],
    page_current=0,
    page_size=PAGE_SIZE,
    page_action='custom'
)


@callback(
    Output('datatable-paging', 'data'),
    Input('datatable-paging', "page_current"),
    Input('datatable-paging', "page_size"))
def update_table(page_current,page_size):
    return df.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')


if __name__ == '__main__':
    app.run(debug=True)