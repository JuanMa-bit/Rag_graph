import os
import json

from pytubefix import YouTube
from pytubefix.cli import on_progress

import moviepy.editor as mp
import os
from openai import OpenAI
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context


local = False

credentials_path="/Users/jucampo/Desktop/Ideas/Podcast/credenciales/credentials.json"
with open(credentials_path, 'r') as file:
    credentials = json.load(file)

os.environ["OPENAI_API_KEY"] = credentials["openAi"]["apiKey"]

class ExtractTextFromVideo:
    def __init__(self):

       self.path_output= "/Users/jucampo/Desktop/Ideas/Podcast/buildRAG/youTubeAudios/"

    def download_youtube_audio(self, youtube_url):
    
        # Create a YouTube object
        yt = YouTube(youtube_url, on_progress_callback = on_progress)
        print(yt.title)

        # Select the best audio stream
        audio_stream = yt.streams.get_audio_only()

        # Download the audio stream to a temporary file
        audio_stream.download(filename='temp_audio',mp3=True,output_path=self.path_output)


    def extract_text_video(self, url):
        try:
            self.download_youtube_audio(url)
            # Create OpenAI Connection
            client = OpenAI()
            client.api_key  = os.environ['OPENAI_API_KEY']

            audio_file= open(self.path_output+"temp_audio.mp3", "rb")
            transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            response_format="text"
            )
            return transcript
        except:
            return ""

