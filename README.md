# Arabic Voice Recorder and Transcriber

A sophisticated web application built with Dash that allows users to record audio and automatically transcribe Arabic speech to text. Perfect for recording and transcribing religious sermons, lectures, or any Arabic audio content.

## Features

- **Audio Recording**
  - High-quality audio recording with real-time status indication
  - Customizable sample rate (currently set to 44.1kHz)
  - Automatic file naming with timestamps
  - Save recordings in WAV format

- **Arabic Transcription**
  - Automatic speech-to-text conversion for Arabic audio
  - Google Speech Recognition integration
  - Save transcriptions in UTF-8 encoded text files
  - View transcriptions in a modal dialog with proper RTL support

- **User Interface**
  - Modern, responsive design using Bootstrap
  - Clear recording status indicators
  - Easy-to-use recording controls
  - List view of all recordings with timestamps
  - Built-in audio player for immediate playback
  - Transcription viewer with Arabic text support

- **File Management**
  - Automatic directory creation for recordings and transcriptions
  - Organized storage structure
  - Audio file cleanup utility for old recordings

## Project Structure

```
├── app.py                 # Main application entry point
├── config.py             # Configuration settings
├── logging_config.py     # Logging setup
├── wsgi.py              # WSGI server configuration
├── components/          # Modular components
│   ├── __init__.py
│   ├── audio_recorder.py   # Recording functionality
│   └── audio_transcriber.py # Transcription functionality
├── recordings/          # Storage for WAV files
├── transcriptions/      # Storage for transcribed text
├── assets/             # Static assets
└── utils/
    └── cleanup.py      # File cleanup utility
```

## Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Khutbaat_Project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Unix/macOS
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application can be configured through various settings in `config.py`:

- `MAX_CONTENT_LENGTH`: Maximum file size limit (default: 16MB)
- `MAX_FILE_AGE_DAYS`: Auto-cleanup threshold for old files (default: 30 days)
- `ALLOWED_EXTENSIONS`: Supported audio file formats (default: WAV)

## Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:8050
   ```

3. Recording Audio:
   - Click "Start Recording" to begin
   - Monitor the recording status indicator
   - Click "Stop Recording" when finished

4. Managing Recordings:
   - View all recordings in the list below the recorder
   - Play recordings directly in the browser
   - Click "Transcribe" to convert speech to text
   - Click "Text" to view saved transcriptions

## Development

The application is built with:
- Dash: Web application framework
- dash-bootstrap-components: UI components
- SpeechRecognition: Audio transcription
- sounddevice: Audio recording
- scipy: Audio file handling
- numpy: Numerical operations

## Production Deployment

For production deployment:
1. Set appropriate environment variables
2. Use WSGI server (e.g., Gunicorn)
3. Configure proper security settings
4. Set up logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
