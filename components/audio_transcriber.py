import speech_recognition as sr
import os
import ffmpeg

class AudioTranscriber:
    def __init__(self):
        # Initialize the recognizer
        self.recognizer = sr.Recognizer()
        # Adjust the recognizer sensitivity
        self.recognizer.energy_threshold = 300
    
    def transcribe_audio(self, audio_path):
        """
        Transcribe the given audio file to Arabic text using Google's Speech Recognition
        """
        try:
            print(f"Attempting to transcribe file at: {audio_path}")
            if not os.path.exists(audio_path):
                print(f"File not found at: {audio_path}")
                return f"Error: File not found at {audio_path}"

            try:
                # Load the audio file directly
                with sr.AudioFile(audio_path) as source:
                    # Adjust for ambient noise
                    self.recognizer.adjust_for_ambient_noise(source)
                    
                    print("Reading audio data...")
                    # Record the entire audio file
                    audio_data = self.recognizer.record(source)
                    
                    # print("Sending to Google Speech Recognition...")
                    # Attempt to recognize the speech using Google's Speech Recognition
                    text = self.recognizer.recognize_google(
                        audio_data,
                        language='ar-AR'  # Arabic language code
                    )
                    # print("Transcription completed successfully")
                    return text

            except sr.UnknownValueError:
                error_msg = "Speech Recognition could not understand the audio"
                print(error_msg)
                return error_msg
                
        except sr.UnknownValueError:
            error_msg = "Speech Recognition could not understand the audio"
            print(error_msg)
            return error_msg
        except sr.RequestError as e:
            error_msg = f"Could not request results from Speech Recognition service; {str(e)}"
            print(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Error during transcription: {str(e)}"
            print(error_msg)
            return error_msg
