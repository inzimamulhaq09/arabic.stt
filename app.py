import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.audio_recorder import AudioRecorder
from flask import send_from_directory
import os

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Add route to serve audio files from recordings directory
@app.server.route('/recordings/<path:path>')
def serve_audio(path):
    return send_from_directory('recordings', path)

# Create an instance of AudioRecorder
audio_recorder = AudioRecorder()

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Voice Recorder", className="text-center mb-4"),
            html.Div([
                dbc.Button("Start Recording", id="start-button", color="success", className="me-2"),
                dbc.Button("Stop Recording", id="stop-button", color="danger", disabled=True),
            ], className="d-flex justify-content-center"),
            html.Div([
                html.P(id="recording-status", className="text-center mt-3"),
            ]),
            html.Hr(className="my-4"),
            html.H4("Recordings", className="mb-3"),
            html.Div(id="recordings-list", className="list-group")
        ])
    ])
], fluid=True, className="py-4")

# Register callbacks from AudioRecorder
audio_recorder.register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True, port=8050)
