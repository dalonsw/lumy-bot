import requests as req
import json
import os


class Speechma:
    def __init__(self, voice_id: str, directory: str):
        self.voice_id = voice_id
        self.directory = directory

    def get_audio(self, url, data, headers):
        try:
            json_data = json.dumps(data)
            response = req.post(url, data=json_data, headers=headers)
            response.raise_for_status()
            if response.headers.get('Content-Type') == 'audio/mpeg':
                return response.content
            else:
                print(f"Unexpected response format: {response.headers.get('Content-Type')}")
                return None
        except req.exceptions.RequestException as e:
            if e.response:
                print(f"Server response: {e.response.text}")
            print(f"Request failed: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def save_audio(self, response):
        if response:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
            file_path = os.path.join(self.directory, f"output.mp3")
            try:
                with open(file_path, 'wb') as f:
                    f.write(response)
                print(f"Audio saved to {file_path}")
            except IOError as e:
                print(f"Error saving audio: {e}")
        else:
            print("No audio data to save")

    def gerar_audio(self, text):
        if not self.voice_id:
            print("Error: No voice selected. Exiting.")
            return


        if not text:
            print("Error: No text provided. Exiting.")
            return

        url = 'https://speechma.com/com.api/tts-api.php'
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "User-Agent": "Python-Requests"
        }

        data = {
            "text": text,
            "voice": self.voice_id
        }

        max_retries = 1
        for retry in range(max_retries):
            response = self.get_audio(url, data, headers)
            if response:
                self.save_audio(response)
                break
            else:
                print(f"Retrying...")