from .server import app
import dash_core_components as dcc
import dash_daq as daq
import dash
from dash.dependencies import Input, Output, State



d1 = dcc.Input(id='from-location', placeholder='Starting Location', size='50', style=dict(height=30)),
d2 = dcc.Input(id='to-location', placeholder='Destination', size='50', style=dict(height=30)),
d3 = daq.ToggleSwitch(id='switch-fields', label='To/From hello', labelPosition='bottom'),


# @app.callback(
#     Output('from-location', 'value'),
#     [Input('switch-fields', 'value')],
#     [State('from-location', 'value'),
#      State('to-location', 'value')]
# )
# def switch_field3(switch, from_location, to_location):
#     user_click = dash.callback_context.triggered[0]['prop_id'].split('.')
#     print(" data ---", user_click)
#     if not switch:
#         print("start to field 1")
#         return from_location
#     else:
#         print("destination to field 1")
#         return to_location


# @app.callback(
#     Output('to-location', 'value'),
#     [Input('switch-fields', 'value')],
#     [State('from-location', 'value'),
#      State('to-location', 'value')]
# )
# def switch_field4(switch, from_location, to_location):
#     if switch:
#         print("start to field 2")
#         return from_location
#     else:
#         print("destination to field 2")
#         return to_location


