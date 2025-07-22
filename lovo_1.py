import requests
from pydub import AudioSegment
from io import BytesIO
import logging
from setup_log import create_logger
from logging.handlers import RotatingFileHandler
import time

bp = Blueprint('routes', __name__)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def audio_return(text, speaker_id):
    url = "https://api.genny.lovo.ai/api/v1/tts/sync"

    payload = {
        "speed": 1,
        "text": text,
        "speaker": speaker_id
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": "e6302ca5-4fb3-4e12-a461-80b821e3dc4f"
    } 

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        data = response.json()["data"][0]
        audio_url = data["urls"][0]

        # Fetch the audio data as a stream
        audio_response = requests.get(audio_url, stream=True)

        if audio_response.status_code == 200:
            audio_data = BytesIO(audio_response.content)
            audio_segment = AudioSegment.from_file(audio_data)
            return audio_segment
        else:
            print("Failed to fetch audio stream")
    else:
        print("Request failed with status code:", response.status_code)
def speaker(gender,locale)
    url = "https://api.genny.lovo.ai/api/v1/speakers?sort=displayName%3A1"

    headers = {
        "accept": "application/json",
        "X-API-KEY": "e6302ca5-4fb3-4e12-a461-80b821e3dc4f"
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()["data"]
        
        # Define the conditions for filtering
        desired_gender = gender  # Change this to the desired gender
        desired_locale = locale  # Change this to the desired locale
        
        # Filter the data based on gender and locale
        filtered_data = [item["id"] for item in data if item["gender"] == desired_gender and item["locale"] == desired_locale]
        
        # Print the filtered IDs
        for speaker_id in filtered_data:
            print("Speaker ID:", speaker_id)
    else:
        print("Error:", response.status_code, response.text)

def change(conversation,speakers_id,Gender,locale,name):
    conversation_audio = AudioSegment.empty()

    # Initialize a variable to keep track of the current speaker
    current_speaker_id = None

    for message in conversation:
        text = message["text"]
        name = message["name"]
    
    # Get the speaker ID based on the name
        speaker_id = name_to_speaker_id.get(name, None)
    
        if speaker_id is None:
            print(f"Speaker ID not found for name: {name}")
            continue
    
        # Check if the speaker has changed
        if current_speaker_id != speaker_id:
        # Add a short pause to indicate a change in speaker
            silence = AudioSegment.silent(duration=500)  # 0.5 seconds of silence
            conversation_audio += silence
    
        # Fetch and append the audio for the current message to the conversation
        audio_stream = audio_return(text, speaker_id)
        conversation_audio += audio_stream
    
        # Update the current speaker
        current_speaker_id = speaker_id

    # Export the merged conversation audio to a single file
    conversation_audio.export("conversation_audio.wav", format="wav")
    print("Conversation audio saved as 'conversation_audio.wav'")

@app.route('/convert', methods=['POST'])
def convert():
    speaker1 = speaker('male','en-US')
    speaker2 = speaker('male','en-IN')









# Define the conversation as a list of text messages with names
# conversation = [
#     {"text": "Hello, how are you?", "name": "Alice"},
#     {"text": "I'm doing well, thank you!", "name": "Bob"},
#     {"text": "What have you been up to lately?", "name": "Alice"},
#     {"text": "I've been busy with work and family.", "name": "Bob"},
#     {"text": "That sounds hectic!", "name": "Alice"},
#     {"text": "Yes, but it's also rewarding.", "name": "Bob"},
#     # Add more messages as needed...
# ]

# Mapping of names to speaker IDs
# name_to_speaker_id = {
#     "Alice": "63b40781241a82001d51b916",
#     "Bob": "63b4094b241a82001d51c5fc",
#     # Add more names and speaker IDs as needed...
# }

# # Initialize an empty audio segment for the conversation
# conversation_audio = AudioSegment.empty()

# # Initialize a variable to keep track of the current speaker
# current_speaker_id = None

# Iterate through the conversation and concatenate audio streams
# for message in conversation:
#     text = message["text"]
#     name = message["name"]
    
#     # Get the speaker ID based on the name
#     speaker_id = name_to_speaker_id.get(name, None)
    
#     if speaker_id is None:
#         print(f"Speaker ID not found for name: {name}")
#         continue
    
#     # Check if the speaker has changed
#     if current_speaker_id != speaker_id:
#         # Add a short pause to indicate a change in speaker
#         silence = AudioSegment.silent(duration=500)  # 0.5 seconds of silence
#         conversation_audio += silence
    
#     # Fetch and append the audio for the current message to the conversation
#     audio_stream = convert(text, speaker_id)
#     conversation_audio += audio_stream
    
#     # Update the current speaker
#     current_speaker_id = speaker_id

# # Export the merged conversation audio to a single file
# conversation_audio.export("conversation_audio.wav", format="wav")
# print("Conversation audio saved as 'conversation_audio.wav'")


@bp.route('/converts', methods=['POST'])
def converts(text, speaker_id):
    url = "https://api.genny.lovo.ai/api/v1/tts/sync"

    payload = {
        "speed": 1,
        "text": text,
        "speaker": speaker_id
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": "e6302ca5-4fb3-4e12-a461-80b821e3dc4f"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        data = response.json()["data"][0]
        audio_url = data["urls"][0]

        # Fetch the audio data as a stream
        audio_response = requests.get(audio_url, stream=True)

        if audio_response.status_code == 200:
            audio_data = BytesIO(audio_response.content)
            audio_segment = AudioSegment.from_file(audio_data)
            return audio_segment
        else:
            print("Failed to fetch audio stream")
    else:
        print("Request failed with status code:", response.status_code)

# Define the conversation as a list of text messages with names
conversation = [
    {"text": "Hello, how are you?", "name": "Alice"},
    {"text": "I'm doing well, thank you!", "name": "Bob"},
    {"text": "What have you been up to lately?", "name": "Alice"},
    {"text": "I've been busy with work and family.", "name": "Bob"},
    {"text": "That sounds hectic!", "name": "Alice"},
    {"text": "Yes, but it's also rewarding.", "name": "Bob"},
    # Add more messages as needed...
]

# Mapping of names to speaker IDs
name_to_speaker_id = {
    "Alice": "63b40781241a82001d51b916",
    "Bob": "63b4094b241a82001d51c5fc",
    # Add more names and speaker IDs as needed...
}

# Initialize an empty audio segment for the conversation
conversation_audio = AudioSegment.empty()

# Initialize a variable to keep track of the current speaker
current_speaker_id = None

# Iterate through the conversation and concatenate audio streams
for message in conversation:
    text = message["text"]
    name = message["name"]
    
    # Get the speaker ID based on the name
    speaker_id = name_to_speaker_id.get(name, None)
    
    if speaker_id is None:
        print(f"Speaker ID not found for name: {name}")
        continue
    
    # Check if the speaker has changed
    if current_speaker_id != speaker_id:
        # Add a short pause to indicate a change in speaker
        silence = AudioSegment.silent(duration=500)  # 0.5 seconds of silence
        conversation_audio += silence
    
    # Fetch and append the audio for the current message to the conversation
    audio_stream = converts(text, speaker_id)
    conversation_audio += audio_stream
    
    # Update the current speaker
    current_speaker_id = speaker_id

# Export the merged conversation audio to a single file
conversation_audio.export("conversation_audio.wav", format="wav")
print("Conversation audio saved as 'conversation_audio.wav'")


logging = create_logger(g)

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)