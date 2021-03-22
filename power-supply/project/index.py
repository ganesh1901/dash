import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from .server import app, server
from .homepage import Homepage
from .admin import Admin
from .others import toggle_sw1



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(
        dbc.Card([
            dbc.CardHeader(
                dbc.Row([
                    dbc.Col(
                        html.A(html.H3("Home"), href="/home"), width=1
                    ),
                    dbc.Col(
                        html.Div(
                            html.H1(" Power Supply utility ", style={'text-align': 'center'})
                        ), width=10
                    ),
                    dbc.Col(
                        html.Div(
                            html.A(html.H3("Admin"), href="/admin")
                        ), width=1
                    )
                ])
            ),
            dbc.CardBody(
                html.Div(id="dbc_body"
                         )
            ),
            dbc.CardFooter(
                html.Div(
                    html.H1(" @IVV/DRDL !Ganesh", style={'text-align': 'center'})
                )
            )
        ])
    )
])


@app.callback(Output('dbc_body', 'children'),
              [Input('url', 'pathname')])
def display_page(value):
    if value == "/admin":
        return Admin()
    elif value == "/home":
        return Homepage()
    else:
        print("Invalid Page Requested!!!", value)

