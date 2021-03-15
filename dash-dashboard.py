import dash
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
from dash.exceptions import PreventUpdate
import os
content_list = {}
act_items = {}
act_no = 0
import struct
PROJECT = ""
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def ParseData(file_name, actno):
    #print("filename", file_name.strip(), '   ', actno)
    file_name = file_name.strip()
    print("filename", file_name, '   ', actno)
    scale_factor = 182.044 #0.00549 #1/1092
    current_scale_factor = 525  # 0.001904762  #1/525
    abs_scale_factor = 22.755  # 0.043945312  #360/8192
    timetag_fmt = "L"
    header_fmt = "H"

    timetag_size = struct.calcsize(timetag_fmt)
    header_size = struct.calcsize(header_fmt)
    packet_size = timetag_size + header_size + 64
    print('packet_size', packet_size)
    line_count = int(os.stat(file_name).st_size / packet_size)
    f = open(file_name, "rb")

    t =[]
    li = [[[], [], [], []], [[], [], [], []], [[], [], [], []], [[], [], [], []]]

    for y in range(line_count):
        bytes = f.read(packet_size)
        if bytes:
            data1 = struct.unpack('16h', bytes[timetag_size + header_size + 8: timetag_size + header_size + 8 + 32])
            data2 = struct.unpack('>4h',
                                  bytes[timetag_size + header_size + 8 + 32: timetag_size + header_size + 8 + 32 + 8])
            t.append(y * 0.01)

            # Absolute Feedback
            li[0][0].append(float(data1[12]) / abs_scale_factor)
            li[0][1].append(float(data1[13]) / abs_scale_factor)
            li[0][2].append(float(data1[14]) / abs_scale_factor)
            li[0][3].append(float(data1[15]) / abs_scale_factor)

            # Incremental Position
            li[1][0].append(float(data1[4]) / scale_factor)
            li[1][1].append(float(data1[5]) / scale_factor)
            li[1][2].append(float(data1[6]) / scale_factor)
            li[1][3].append(float(data1[7]) / scale_factor)

            # current
            li[3][0].append(float(data1[8]) / current_scale_factor)
            li[3][1].append(float(data1[9]) / current_scale_factor)
            li[3][2].append(float(data1[10]) / current_scale_factor)
            li[3][3].append(float(data1[11]) / current_scale_factor)

            # OBC Command
            li[2][0].append(float(data1[0]) / scale_factor)
            li[2][1].append(float(data1[1]) / scale_factor)
            li[2][2].append(float(data1[2]) / scale_factor)
            li[2][3].append(float(data1[3]) / scale_factor)
        else:
            print(" File read completed")
            f.close()

    return t, li


def Table_Obj(idname):
    global content_list
    coloumn_name = ["S.No", "File Name", "Date&Time", "Conducted Place", "Stake Holders", "Remarks"]
    return html.Div([dash_table.DataTable(
            id=idname,
            columns=[{
                'name': coloumn_name[i].format(i),
                'id': 'column-{}'.format(i),
                'renamable': True,
            } for i in range(len(coloumn_name))],
            export_format='xlsx',
            export_headers='display',
            merge_duplicate_headers=True,
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
            row_selectable="single"
            )
        ])


def drawDataList(name_list):
    global content_list
    project_list = []
    for i in os.walk('./PROJECTS'):
        project_list = i[1]
        break
    print(project_list)
    items = []
    for i in project_list:
        items.append(i)
        content_list[i] = []

    dropdowns = html.Div(
        [
           dcc.Dropdown(
                options=[{'label': k, 'value': k} for k in items], id="project_menu",
            ),
        ],
        #style={"display": "flex", "flexWrap": "wrap"},
    )
    return html.Div([
        dropdowns
    ])

# Text field
def drawText(name):
    return html.Div([
                 html.H2(name),
        ], style={'textAlign': 'center', 'border':'none'})


def drawButton(button_name):
    return html.Div(
        html.Button(button_name, id='plot-by-click', n_clicks=0),
        style={'font-size':'18px', 'width': '150px'}
    )

def drawComboBox():
    global act_items
    act_items[1] = "Channel 1"
    act_items[2] = "Channel 2"
    act_items[3] = "Channel 3"
    act_items[4] = "Channel 4"
    act_items[5] = "All Channels"
    return html.Div([
        dcc.Dropdown(
            options=[{'label':val, 'value': key} for key,val in act_items.items()], id="act-sel",
        )
    ], style={"display" : "none"}, id="ACT")

def drawPlot():
    return html.Div([],  id='plot-graph')


app = dash.Dash(external_stylesheets=[dbc.themes.SOLAR])
app.layout = html.Div([
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.H1(" Plot Utility Browser")
                        ], style={'textAlign': 'center',
                                    'border' : 'none'}), width=12
                )
            ]),
            dbc.Row([
                dbc.Col(width=2),
                dbc.Col([
                    drawText("Projects")
                ], width=2),
                dbc.Col([
                    drawDataList([])
                ], width=3),
                dbc.Col(
                    html.Div(
                        html.H2("Act-Selct")
                    ),id="act_sel_name", style={"display": "none"}, width=1
                ),
                dbc.Col([
                    drawComboBox()
                    #drawButton("plot")
                ],width=3)
            ]),
            dbc.Row(
                dbc.Col(
                    Table_Obj('data_table'), width=12
                )
            ),
            dbc.Row([
                html.Div([
                    html.H2(" ")
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    drawPlot()
                ], width=12)
            ])
        ])
    ]),
    html.Div(id='output_div')
])


def GetContent(ProjectName):
    print('************** called ************')
    global content_list,PROJECT
    PROJECT = ProjectName
    for key in content_list.keys():
        content_list[key] = []

    f = open('PROJECTS/'+ProjectName+'/index.csv', "r")
    while True:
        data = f.readline()
        if data:
            aa = data.rstrip().split(',')
            content_list[ProjectName].append(aa)
        else:
            print('End of list')
            break


@app.callback(
    Output("data_table", "data"),
    Output("project_menu", "value"),
    Output('ACT', 'style'),
    Output('act_sel_name', 'style'),
    Input("project_menu", 'value')
)
def ProjectMenu(label):
    print('&&&&&&&', label)
    if label is None:
        raise PreventUpdate
    else:
        GetContent(label)
        #print('content list', content_list[label])
        data = [{'column-{}'.format(i): (content_list[label][j][i]) for i in range(len(content_list[label][j]))}
                for j in range(len(content_list[label]))
                ]
        style = {"display":"inline"};
        return data, label, style, style


@app.callback(
    Output('output_div', 'children'),
    Input('data_table', 'active_cell'),
    State('data_table', 'data')
)

def getActiveCell(active_cell, data):
    if active_cell:
        col = active_cell['column_id']
        row = active_cell['row']
        cellData = data[row][col]
        return html.P(f'row: {row}, col: {col}, value: {cellData}')
    return html.P('no cell selected')


@app.callback(
    Output('act-sel', 'value'),
    Input('act-sel', 'value')
)
def SetActInput(act_val):
    global  act_items
    global  act_no
    if act_val is None:
        raise PreventUpdate
    act_no = act_val
    #print("$$$$$$$$", act_val, act_items[act_val])
    return act_val


@app.callback(
    Output('plot-graph', 'children'),
    [Input('data_table', 'selected_rows'), Input('act-sel', 'value')],
    [State("plot-graph", "children"), State('data_table', 'data')]
)
def generatePlot(selected_rows, act_val, children, data):
    global act_no
    #print('rows', children)
    if data is None:
        raise PreventUpdate
    if selected_rows is None:
        raise PreventUpdate

    filename = "PROJECTS/" + PROJECT + '/' + data[selected_rows[0]]['column-1'].strip()
    print('***********', (filename), act_no)
    time, data_list = ParseData(filename, act_no)

    if act_no != 5:
        fig = make_subplots(rows=1, cols=1, start_cell="bottom-left", subplot_titles=("Channel no %d " % act_no))
        fig.update_layout(title_text="Actuator Channel %d !! %s"% (act_no, data[selected_rows[0]]['column-1'].strip()))
        fig.add_trace(go.Scatter(x=time, y=data_list[3][act_no-1], name="ACT %d Current" % act_no), row=1, col=1)
        fig.add_trace(go.Scatter(x=time, y=data_list[0][act_no-1], name="ACT %d Abs FB" % act_no), row=1, col=1)
        fig.add_trace(go.Scatter(x=time, y=data_list[1][act_no-1], name="ACT %d Inc FB" % act_no), row=1, col=1)
        fig.add_trace(go.Scatter(x=time, y=data_list[2][act_no-1],  name="ACT %d Command" % act_no), row=1, col=1)

    else:
        fig = make_subplots(rows=2, cols=2, start_cell="top-left", subplot_titles=("Channel 1","Channel 2", "Channel 3", "Channel 4"))
        fig.update_layout(title_text="Actuator All Channels !!! %s " % data[selected_rows[0]]['column-1'].strip())
        fig.add_trace(go.Scatter(x=time, y=data_list[3][0], name="ACT 1 Current"), row=1, col=1)
        fig.add_trace(go.Scatter(x=time, y=data_list[0][0], name="ACT 1 Abs FB"), row=1, col=1)
        fig.add_trace(go.Scatter(x=time, y=data_list[1][0], name="ACT 1 Inm FB"), row=1, col=1)
        fig.add_trace(go.Scatter(x=time, y=data_list[2][0], name="ACT 1 Command"), row=1, col=1)

        fig.add_trace(go.Scatter(x=time, y=data_list[3][1], name="ACT 2 Current"), row=1, col=2)
        fig.add_trace(go.Scatter(x=time, y=data_list[0][1], name="ACT 2 Abs FB"), row=1, col=2)
        fig.add_trace(go.Scatter(x=time, y=data_list[1][1], name="ACT 2 Inm FB"), row=1, col=2)
        fig.add_trace(go.Scatter(x=time, y=data_list[2][1], name="ACT 2 Command"), row=1, col=2)

        fig.add_trace(go.Scatter(x=time, y=data_list[3][2], name="ACT 3 Current"), row=2, col=1)
        fig.add_trace(go.Scatter(x=time, y=data_list[0][2], name="ACT 3 Abs FB"), row=2, col=1)
        fig.add_trace(go.Scatter(x=time, y=data_list[1][2], name="ACT 3 Inm FB"), row=2, col=1)
        fig.add_trace(go.Scatter(x=time, y=data_list[2][2], name="ACT 3 Command"), row=2, col=1)

        fig.add_trace(go.Scatter(x=time, y=data_list[3][3], name="ACT 4 Current"), row=2, col=2)
        fig.add_trace(go.Scatter(x=time, y=data_list[0][3], name="ACT 4 Abs FB"), row=2, col=2)
        fig.add_trace(go.Scatter(x=time, y=data_list[1][3], name="ACT 4 Inm FB"), row=2, col=2)
        fig.add_trace(go.Scatter(x=time, y=data_list[2][3], name="ACT 4 Command"), row=2, col=2)

    if children != []:
        children[0] =  dcc.Graph(
                figure= fig
            )
    else:
        children.append(
            dcc.Graph(
               figure=fig
            )
        )
    return children

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)