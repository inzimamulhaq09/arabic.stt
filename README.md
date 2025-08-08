# Voice Recorder Application

A Dash web application that allows users to record audio using their microphone and save the recordings to a folder.

## Features

- Start/Stop recording functionality
- Visual indication of recording status
- Automatic saving of recordings with timestamps
- Modern UI with Bootstrap styling

## Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your web browser and navigate to `http://127.0.0.1:8050`

## Project Structure

- `app.py`: Main application file
- `components/`: Contains modular components
  - `audio_recorder.py`: Audio recording functionality
- `recordings/`: Directory where recorded audio files are saved
- `assets/`: Static assets (if any)

## Dependencies

- dash
- dash-bootstrap-components
- sounddevice
- scipy
- numpy
- python-dotenv

## Usage

1. Click the "Start Recording" button to begin recording audio
2. The recording status will be displayed on the page
3. Click "Stop Recording" to end the recording
4. The audio file will be automatically saved in the `recordings` folder with a timestamp
