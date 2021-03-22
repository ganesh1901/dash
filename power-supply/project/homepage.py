import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import dash_daq as daq
from dash.dependencies import Input, Output, State
from .dbconnecter import DB_Connection
from .server import app
from .others import *
from dash.exceptions import PreventUpdate


def Gettable():
    db_conn = DB_Connection()
    cursor = db_conn.cursor()
    cursor.execute(''' select * from External_Supply''')
    print('row', cursor.fetchall())


def ToggleSwitch(idname):
    dd = daq.ToggleSwitch(id=idname, color='green', label="ON-OFF", labelPosition='top')

    @app.callback(
        Output(idname, 'label'),
        Input(idname, 'value')
    )
    def Callback(state):
        print(" toggle swich *********", state)
        if state is None:
            raise PreventUpdate
        if state:
            return "OFF"
        else:
            return "ON"

    return html.Div(dd)




def Datatable(idname):
    coloumn_name = ['S.No', "Name", "SubSystems", "Prog Voltage",
                    "Prog Current", "Volatge", "Current", " "]

    tt = dash_table.DataTable(
            id=idname,
            columns=[{
                'name': coloumn_name[i].format(i),
                'id': idname+'column-{}'.format(i),
                'renamable': True,
            } for i in range(len(coloumn_name))],
            # export_format='xlsx',
            # export_headers='display',
            # merge_duplicate_headers=True,
            editable=False,
            style_cell={'textAlign': 'center',
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'},
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(255, 0, 255)'
                }
            ],
            sort_action="native",
            #row_selectable="single"
            )
    return t1

def FillTabeleData():
    pass


def Homepage():
    Gettable()
    layout = html.Div([
        html.H2(" Hello world Home Page !!!!"),
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(id="External", width=6),
                    dbc.Col(id="Internal", width=6)
                ]),
                dbc.Row([
                    dbc.Col(id="E1_graph", width=4),
                    dbc.Col(id="E2_graph", width=4),
                    dbc.Col(id="E3_graph", width=4)
                ]),
                dbc.Row([
                    dbc.Col(id="I1_graph", width=4),
                    dbc.Col(id="I2_graph", width=4),
                    dbc.Col(id="I3_graph", width=4)
                ])
            ]),
        ]),
        ToggleSwitch(toggle_sw1),
        ToggleSwitch(toggle_sw2)
    ])
    return layout