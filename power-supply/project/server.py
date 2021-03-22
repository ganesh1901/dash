from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc


server = Flask('myproject')
app = Dash(server=server, external_stylesheets=[dbc.themes.DARKLY])
app.config.suppress_callback_exceptions = True
