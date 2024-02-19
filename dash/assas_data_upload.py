import dash
import dash_bootstrap_components as dbc
from dash import Dash, dash_table, html, dcc, Input, Output, callback, State
import pandas as pd
import numpy as np
from collections import OrderedDict
import h5py
import os
import base64
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory

import logging

logger = logging.getLogger(__name__)

from assasdb import AssasDatabaseManager

UPLOAD_DIRECTORY = "/home/jonas/upload"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

server = Flask(__name__)
app = Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

app.layout = html.Div([
    html.H2('ASSAS Database - Upload ASTEC Dataset'),
    dbc.Alert("Upload interface for ASTEC training datasets", color="primary", style={'textAlign': 'center'}),
    dbc.InputGroup(
            [dbc.InputGroupText("@"), dbc.Input(placeholder="Username")],
            className="mb-3",
    ),
    dbc.InputGroup(
            [
                dbc.Input(placeholder="Recipient's username"),
                dbc.InputGroupText("@example.com"),
            ],
            className="mb-3",
    ),
    dbc.InputGroup(
            [
                dbc.InputGroupText("$"),
                dbc.Input(placeholder="Amount", type="number"),
                dbc.InputGroupText(".00"),
            ],
            className="mb-3",
    ),
    dbc.InputGroup(
            [
                dbc.InputGroupText("Total:"),
                dbc.InputGroupText("$"),
                dbc.Input(placeholder="Amount", type="number"),
                dbc.InputGroupText(".00"),
                dbc.InputGroupText("only"),
            ],
            className="mb-3",
    ),
    dbc.InputGroup(
            [
                dbc.InputGroupText("With textarea"),
                dbc.Textarea(),
            ],
            className="mb-3",
    ),
    dbc.InputGroup(
            [
                dbc.Select(
                    options=[
                        {"label": "Option 1", "value": 1},
                        {"label": "Option 2", "value": 2},
                    ]
                ),
                dbc.InputGroupText("With select"),
            ]
    ),
    html.Hr(),
    dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            }),
    html.Hr(),
    dcc.Interval(id="progress-interval", n_intervals=0, interval=500),
    dbc.Progress(id="progress"),
    html.Hr(),
    html.H2("File List"),
    html.Ul(id="file-list")
])

def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

if __name__ == '__main__':
    app.run(debug=True, port=8052)