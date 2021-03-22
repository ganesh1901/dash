from .server import app, server
from . import callback1
from . import callback2
import dash_html_components as html


app.config['suppress_callback_exceptions'] = True
app.layout = html.Div([
    html.H1('hello Bye!!!!'),
    html.Div(callback1.d1),
    html.Div(callback1.d2),
    html.Div(callback1.d3)
])
