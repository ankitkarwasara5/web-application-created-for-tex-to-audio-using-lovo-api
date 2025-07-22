from flask import Flask, render_template, request, Response, send_file, Blueprint
import requests, json
from io import BytesIO
from pydub import AudioSegment
import requests
from flask import Blueprint, request, jsonify


app = Flask(__name__)
bp = Blueprint('routes', __name__)


def get_audio(conversation, name_to_speaker_id):
    
    url = "https://api.genny.lovo.ai/api/v1/tts/sync"

    # Initialize an empty audio segment for the conversation
    conversation_audio = AudioSegment.empty()

    # Initialize a variable to keep track of the current speaker
    current_speaker_id = None

    # Iterate through the conversation and concatenate audio streams
    for message in conversation:
        if "text" in message:
            text = message["text"]  # Get the text from the current message
            name = message["name"]

            # Get the speaker ID based on the name
            speaker_id = name_to_speaker_id.get(name, None)

            if speaker_id is None:
                print(f"Speaker ID not found for name: {name}")
                continue

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

                    # Append the audio for the current message to the conversation
                    conversation_audio += audio_segment

                    # Update the current speaker
                    current_speaker_id = speaker_id
                else:
                    print("Failed to fetch audio stream")
            else:
                print("Request failed with status code:", response.status_code)
        else:
            print("text not present")

    return conversation_audio


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    speaker_data = request.form.get('speaker_data')
    conversation = request.form.get('conversation')

    # Ensure that the input is not empty
    if not speaker_data or not conversation:
        return "Both speaker data and conversation are required", 400  # Return a 400 Bad Request response

    # Convert the input data to dictionaries and lists
    try:
        speaker_data_dict = json.loads(speaker_data)
        conversation_list = json.loads(conversation)
    except json.JSONDecodeError as e:
        return "Error parsing input data: " + str(e), 400

    urls = "https://api.genny.lovo.ai/api/v1/speakers?sort=displayName%3A1"

    headers = {
        "accept": "application/json",
        "X-API-KEY": "e6302ca5-4fb3-4e12-a461-80b821e3dc4f"
    }

    response = requests.get(urls, headers=headers)

    if response.status_code == 201 or response.status_code == 200:
        data = response.json()["data"]
        name_to_speaker_id = {}

        for speaker_name, speaker_info in speaker_data_dict.items():
            if "gender" in speaker_info:
                desired_gender = speaker_info["gender"]
                desired_locale = speaker_info["accent"]

                matching_speakers = [item["id"] for item in data if item["gender"] == desired_gender and item["locale"] == desired_locale]
                for speaker_id in matching_speakers:
                    name_to_speaker_id[speaker_name] = matching_speakers[0]
            else:
                print("wrong gender")
        print("Data Saved into name_to_speaker_id")
    else:
        print("Error:", response.status_code, response.text)

    if not isinstance(name_to_speaker_id, dict):
        return "name_to_speaker_id should be a dictionary", 400 

    conversation_audio = get_audio(conversation_list, name_to_speaker_id)

    # Save the conversation audio to a file on your desktop
    conversation_audio.export("conversation_audio.wav", format="wav")

    # Provide a download link for the user
    return send_file(
        "conversation_audio.wav",
        as_attachment=True,
        download_name="conversation_audio.wav",
        mimetype="audio/wav"
    )

@bp.route('/converts', methods=['POST'])
def converts():
    speaker_data_str = request.json.get('speaker_data_json')
    conversation_str = request.json.get('conversation_json')

    try:
        speaker_data = json.loads(speaker_data_str)
    except Exception as e:
        return "Error parsing name_to_speaker_id: " + str(e), 400  # Return a 400 Bad Request response

    if not isinstance(speaker_data, dict):
        return "name_to_speaker_id should be a dictionary", 400  # Return a 400 Bad Request response

    urls = "https://api.genny.lovo.ai/api/v1/speakers?sort=displayName%3A1"

    headers = {
        "accept": "application/json",
        "X-API-KEY": "e6302ca5-4fb3-4e12-a461-80b821e3dc4f"
    }

    response = requests.get(urls, headers=headers)

    if response.status_code == 201 or response.status_code == 200:
        data = response.json()["data"]
        name_to_speaker_id = {}

        for speaker_name, speaker_info in speaker_data.items():
            if "gender" in speaker_info:
                desired_gender = speaker_info["gender"]
                desired_locale = speaker_info["accent"]

                matching_speakers = [item["id"] for item in data if item["gender"] == desired_gender and item["locale"] == desired_locale]
                for speaker_id in matching_speakers:
                    name_to_speaker_id[speaker_name] = matching_speakers[0]
            else:
                print("wrong gender")
        print("Data Saved into name_to_speker_id")
    else:
        print("Error:", response.status_code, response.text)

    if not isinstance(name_to_speaker_id, dict):
        return "name_to_speaker_id should be a dictionary", 400  # Return a 400 Bad Request response

    try:
        conversation = json.loads(conversation_str)
    except Exception as e:
        return "Error parsing conversation: " + str(e), 400

    conversation_audio = get_audio(conversation, name_to_speaker_id)

    # Save the conversation audio to a file on your desktop
    conversation_audio.export("conversation_audio.wav", format="wav")

    # Provide a download link for the user
    return send_file(
        "conversation_audio.wav",
        as_attachment=True,
        download_name="conversation_audio.wav",
        mimetype="audio/wav"
    )


app.register_blueprint(bp)
if __name__ == '__main__':
    app.run(debug=True)
