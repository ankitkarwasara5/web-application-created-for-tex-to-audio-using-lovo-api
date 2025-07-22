import requests
import json
from pydub import AudioSegment

BASE_URL = "http://127.0.0.1:5000"

# Define the conversation as a list of text messages with names
conversation = [
    {"text": "Hello, how are you?", "name": "Alice"},
    {"text": "I'm doing well, thank you!", "name": "Bob"},
    {"text": "What have you been up to lately?", "name": "Alice"},
    {"text": "I've been busy with work and family.", "name": "Bob"},
    {"text": "That sounds hectic!", "name": "Alice"},
    {"text": "Yes, but it's also rewarding and enjoying.", "name": "Bob"}
]

# Define the speaker data as a dictionary
speaker_data = {
    "Alice": {"gender": "male", "accent": "en-IN"},
    "Bob": {"gender": "female", "accent": "en-IN"}}

# Convert speaker_data and conversation to JSON-encoded strings
speaker_data_json = json.dumps(speaker_data)
conversation_json = json.dumps(conversation)

# Create a data dictionary to send both conversation and speaker data
data = {
    "speaker_data_json": speaker_data_json,
    "conversation_json": conversation_json
}

# Set the headers with the Content-Type as application/json
headers = {
    "Content-Type": "application/json",
    "X-API-KEY": "e6302ca5-4fb3-4e12-a461-80b821e3dc4f"
}

# Make the POST request with headers
response = requests.post(f"{BASE_URL}/converts", data=json.dumps(data), headers=headers)

if response.status_code == 200 or response.status_code == 201:
    with open("conversation_audio.wav", "wb") as audio_file:
        audio_file.write(response.content)
    print("Audio saved to conversation_audio.wav")
else:
    print("Failed to retrieve audio data:", response.status_code)
    print(response.content)
