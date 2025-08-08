import dash
from dash.dependencies import Input, Output, State
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import os
from datetime import datetime
import glob
from dash import html
import dash_bootstrap_components as dbc
from .audio_transcriber import AudioTranscriber

class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.sample_rate = 44100
        self.recording = []
        # Use absolute paths for directories in the root project folder
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.recordings_dir = os.path.join(root_dir, 'recordings')
        self.transcriptions_dir = os.path.join(root_dir, 'transcriptions')
        os.makedirs(self.recordings_dir, exist_ok=True)
        os.makedirs(self.transcriptions_dir, exist_ok=True)
        # print(f"Recordings directory: {self.recordings_dir}")
        # print(f"Transcriptions directory: {self.transcriptions_dir}")
        self.transcriber = AudioTranscriber()
        
    def get_recordings_list(self):
        # Get all wav files in the recordings directory using absolute path
        recordings_path = os.path.join(os.getcwd(), self.recordings_dir)
        wav_files = glob.glob(os.path.join(recordings_path, '*.wav'))
        # Sort files by modification time (newest first)
        wav_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        recordings_list = []
        for wav_file in wav_files:
            filename = os.path.basename(wav_file)
            # Format the file modification time
            mod_time = datetime.fromtimestamp(os.path.getmtime(wav_file))
            time_str = mod_time.strftime("%Y-%m-%d %H:%M:%S")
            
            recordings_list.append(
                dbc.ListGroupItem([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Strong(filename),
                                html.Small(f" (Recorded: {time_str})", className="text-muted")
                            ])
                        ], width=3),
                        dbc.Col([
                            html.Audio(
                                id={'type': 'audio-player', 'index': filename},
                                src=f'/recordings/{filename}',
                                controls=True,
                                style={'width': '100%'},
                                autoPlay=False
                            )
                        ], width=6),
                        dbc.Col([
                            html.Div([
                                dbc.Button(
                                    "Transcribe",
                                    id={'type': 'transcribe-button', 'index': filename},
                                    color="info",
                                    className="me-2"
                                ),
                                dbc.Button(
                                    "Text",
                                    id={'type': 'view-text-button', 'index': filename},
                                    color="secondary",
                                    className="me-2",
                                    disabled=not os.path.exists(os.path.join(self.transcriptions_dir, os.path.splitext(filename)[0] + '.txt'))
                                ),
                                html.Div(
                                    id={'type': 'transcription-output', 'index': filename},
                                    className="mt-2"
                                )
                            ])
                        ], width=3)
                    ], align="center")  # Vertically center align the row contents
                ])
            )
        return recordings_list if recordings_list else [html.P("No recordings found.", className="text-muted")]

    def read_transcription_file(self, filename):
        """Read transcription from file"""
        try:
            file_path = os.path.join(self.transcriptions_dir, os.path.splitext(filename)[0] + '.txt')
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return None
        except Exception as e:
            print(f"Error reading transcription file: {str(e)}")
            return None

    def register_callbacks(self, app):
        # Combined callback for transcribe and view text buttons
        @app.callback(
            Output({'type': 'transcription-output', 'index': dash.MATCH}, 'children'),
            [Input({'type': 'transcribe-button', 'index': dash.MATCH}, 'n_clicks'),
             Input({'type': 'view-text-button', 'index': dash.MATCH}, 'n_clicks')],
            [State({'type': 'transcribe-button', 'index': dash.MATCH}, 'id')],
            prevent_initial_call=True
        )
        def handle_transcription_actions(transcribe_clicks, view_clicks, button_id):
            # Get the ID of the button that triggered the callback
            ctx = dash.callback_context
            if not ctx.triggered:
                return dash.no_update
                
            triggered_id = ctx.triggered[0]['prop_id']
            filename = button_id['index']
            
            # Handle view text button
            if 'view-text-button' in triggered_id and view_clicks:
                transcription = self.read_transcription_file(filename)
                if transcription:
                    return dbc.Modal([
                        dbc.ModalHeader(
                            dbc.ModalTitle("Saved Transcription"),
                            close_button=True
                        ),
                        dbc.ModalBody([
                            html.P("Transcription:", className="fw-bold"),
                            html.P(
                                transcription, 
                                dir="rtl", 
                                lang="ar", 
                                className="text-end border p-3 bg-light"
                            )
                        ])
                    ],
                    id={'type': 'transcription-modal', 'index': filename},
                    size="lg",
                    is_open=True)
                    
            # Handle transcribe button
            if 'transcribe-button' in triggered_id and transcribe_clicks:
                file_path = os.path.join(self.recordings_dir, filename)
                transcription = self.transcriber.transcribe_audio(file_path)
                
                # Save transcription to file
                transcription_filename = os.path.splitext(filename)[0] + '.txt'
                transcription_path = os.path.join(self.transcriptions_dir, transcription_filename)
                with open(transcription_path, 'w', encoding='utf-8') as f:
                    f.write(transcription)
                
                return dbc.Modal([
                    dbc.ModalHeader(
                        dbc.ModalTitle("Transcription Result"),
                        close_button=True
                    ),
                    dbc.ModalBody([
                        html.P("Transcription:", className="fw-bold"),
                        html.P(
                            transcription, 
                            dir="rtl", 
                            lang="ar", 
                            className="text-end border p-3 bg-light"
                        ),
                        html.Small(f"Saved to: {transcription_filename}", className="text-muted d-block mt-2")
                    ])
                ],
                id={'type': 'transcription-modal', 'index': filename},
                size="lg",
                is_open=True)

        # Callback for start button and recording status
        @app.callback(
            [Output("start-button", "disabled"),
             Output("stop-button", "disabled"),
             Output("recording-status", "children"),
             Output("recordings-list", "children")],
            [Input("start-button", "n_clicks"),
             Input("stop-button", "n_clicks")],
            [State("start-button", "disabled")]
        )
        def handle_recording_buttons(start_clicks, stop_clicks, start_disabled):
            # Get the ID of the button that triggered the callback
            triggered_id = dash.callback_context.triggered_id
            
            recordings_list = self.get_recordings_list()
            
            if triggered_id == "start-button" and not start_disabled:
                self._start_recording()
                return True, False, "Recording in progress...", recordings_list
            
            elif triggered_id == "stop-button":
                self._stop_recording()
                return False, True, "Recording saved!", recordings_list
            
            # Initial state
            return False, True, "Click 'Start Recording' to begin", recordings_list
    
    def _start_recording(self):
        self.is_recording = True
        self.recording = []
        
        def audio_callback(indata, frames, time, status):
            if self.is_recording:
                self.recording.append(indata.copy())
        
        # Start recording
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            callback=audio_callback
        )
        self.stream.start()
    
    def _stop_recording(self):
        if hasattr(self, 'stream'):
            self.is_recording = False
            self.stream.stop()
            self.stream.close()
            
            try:
                # Convert list of arrays into one array
                recording_array = np.concatenate(self.recording, axis=0)
                
                # Normalize the audio data
                recording_array = np.int16(recording_array * 32767)
                
                # Create recordings directory if it doesn't exist
                os.makedirs(self.recordings_dir, exist_ok=True)
                
                # Save the recording with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"recording_{timestamp}.wav"
                filepath = os.path.join(self.recordings_dir, filename)
                
                # Save in recordings folder with proper format
                wavfile.write(
                    filepath,
                    self.sample_rate,
                    recording_array
                )
                
                print(f"Recording saved successfully at: {filepath}")
            except Exception as e:
                print(f"Error saving recording: {str(e)}")
