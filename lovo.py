import requests
from pydub import AudioSegment
from io import BytesIO

def get_audio_stream(text, speaker_id):
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

# Define the conversation as a list of text messages
conversation = [
    {"text": "Hello, how are you?", "speaker_id": "640f477d2babeb0024be422b"},
    {"text": "I'm doing well, thank you!", "speaker_id": "63b4094b241a82001d51c5fc"},
    {"text": "What have you been up to lately?", "speaker_id": "640f477d2babeb0024be422b"},
    {"text": "I've been busy with work and family.", "speaker_id": "63b4094b241a82001d51c5fc"},
    {"text": "That sounds hectic!", "speaker_id": "640f477d2babeb0024be422b"},
    {"text": "Yes, but it's also rewarding.", "speaker_id": "63b4094b241a82001d51c5fc"},
    # Add more messages as needed...
]

# Initialize an empty audio segment for the conversation
conversation_audio = AudioSegment.empty()

# Iterate through the conversation and concatenate audio streams
for message in conversation:
    text = message["text"]
    speaker_id = message["speaker_id"]
    audio_stream = get_audio_stream(text, speaker_id)
    
    # Append the audio for the current message to the conversation
    conversation_audio += audio_stream

# Export the merged conversation audio to a single file
conversation_audio.export("conversation_audio.wav", format="wav")
print("Conversation audio saved as 'conversation_audio.wav'")







# # Example usage to get two audio streams
# audio1 = get_audio_stream("Hello, how are you?", "640f477d2babeb0024be422b")
# audio2 = get_audio_stream("I'm doing well, thank you!", "63b4094b241a82001d51c5fc")

# # Merge the audio streams
# merged_audio = audio1 + audio2

# # Export the merged audio to a new file
# merged_audio.export("merged_audio.wav", format="wav")
# print("Merged audio saved as 'merged_audio.wav'")
