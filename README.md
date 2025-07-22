# Text-to-Speech Conversation Converter

This project is a web-based application that converts a structured text conversation into a single audio file. It uses the Lovo AI API to generate speech for each part of the conversation, dynamically assigning voices to different speakers based on specified gender and accent. The final output is a downloadable `.wav` audio file containing the complete conversation.

## Features

-   **Multi-Speaker Conversations:** Handles conversations with multiple speakers.
-   **Dynamic Voice Assignment:** Automatically assigns a unique voice to each speaker based on desired gender and accent (e.g., male, en-IN).
-   **Audio Concatenation:** Seamlessly stitches together audio segments from different speakers into one continuous audio file.
-   **Web Interface:** A simple HTML form to input speaker data and the conversation script in JSON format.
-   **Downloadable Output:** Provides the final audio as a downloadable `.wav` file.
-   **Request Logging:** Logs application events and errors for easier debugging.

## Technologies Used

-   **Backend:** Python, Flask
-   **API:** [Lovo AI API](https://lovo.ai/docs/api-reference/text-to-speech) for Text-to-Speech generation.
-   **Libraries:**
    -   `requests`: For making HTTP requests to the Lovo AI API.
    -   `pydub`: For manipulating and combining audio files.
-   **Frontend:** HTML

## Setup and Installation

Follow these steps to set up and run the project on your local machine.

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    Install all the required packages from the `requirement.txt` file.
    ```bash
    pip install -r requirement.txt
    ```
    *Note: `pydub` requires FFmpeg for handling different audio formats. Make sure you have FFmpeg installed on your system. You can download it from [ffmpeg.org](https://ffmpeg.org/download.html).*

4.  **API Key:**
    The application requires an API key from Lovo AI. The key is currently hardcoded in `app.py` and `speaker_id.py`. It is highly recommended to manage this securely, for example, using environment variables.

5.  **Run the Application:**
    Execute the `app.py` script to start the Flask development server.
    ```bash
    python app.py
    ```
    The application will be running at `http://127.0.0.1:5000`.

## Usage

Once the application is running, open your web browser and navigate to `http://127.0.0.1:5000`.

1.  **Speaker Data (JSON):**
    In this field, define the speakers in your conversation. For each speaker, you must provide a `gender` and an `accent` (locale). The application will use this information to find a matching voice from the API.

    **Example:**
    ```json
    {
      "John": {
        "gender": "male",
        "accent": "en-US"
      },
      "Jane": {
        "gender": "female",
        "accent": "en-GB"
      }
    }
    ```

2.  **Conversation JSON:**
    In this field, provide the conversation script as a list of JSON objects. Each object must contain a `name` (which corresponds to a speaker defined in the Speaker Data) and the `text` they speak.

    **Example:**
    ```json
    [
      {
        "name": "John",
        "text": "Hello Jane, how are you today?"
      },
      {
        "name": "Jane",
        "text": "I'm doing great, John! Thanks for asking."
      },
      {
        "name": "John",
        "text": "Wonderful. Let's get started with our project."
      }
    ]
    ```

3.  **Convert to Audio:**
    Click the "Convert to Audio" button. The application will process the inputs, generate the audio, and prompt you to download the resulting `conversation_audio.wav` file.

## API Endpoints

### `/convert`

-   **Method:** `POST`
-   **Description:** The main endpoint that receives speaker and conversation data, processes it, and returns an audio file.
-   **Form Data:**
    -   `speaker_data`: A JSON string defining the speakers.
    -   `conversation`: A JSON string containing the conversation script.
-   **Success Response:** A `.wav` file attachment for download.
-   **Error Response:** An HTTP 400 status with an error message if the input data is invalid.

## Logging

The application is configured to log important events and errors. The logs are stored in `base.log` with a rotating file handler that limits the file size and backup count. This is useful for monitoring the application's behavior and troubleshooting issues.

## Future Improvements

-   **Secure API Key Management:** Implement environment variables or a configuration file to manage the Lovo AI API key instead of hardcoding it.
-   **Dynamic Voice Selection:** Allow users to select specific voices from a dropdown list populated via the API, rather than just relying on the first available match for gender and accent.
-   **Support for More Audio Formats:** Add options to download the audio in different formats like MP3.
-   **Asynchronous Processing:** For very long conversations, the API calls could be handled asynchronously to prevent the request from timing out and to improve user experience.
-   **Enhanced UI:** Improve the frontend to provide better feedback to the user, such as loading indicators and a more user-friendly way to build the conversation script.
-   **Error Handling:** Implement more specific error handling to give users clearer feedback (e.g., "Speaker 'X' not found in Speaker Data").
