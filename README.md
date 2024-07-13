# DigiWell Mental Health Chatbot

DigiWell is a mental health chatbot designed to engage in therapeutic sessions, similar to how a psychologist or counselor would. The chatbot initiates conversations, encourages users to express their emotions, and provides solutions to their concerns. It also offers diagnoses and treatment options if requested.

## Features

- Records user audio input
- Transcribes audio to text using OpenAI's Whisper
- Generates responses using OpenAI and Azure OpenAI models
- Converts text responses to speech using OpenAI's TTS model
- Automatically plays audio responses
- Displays the full conversation history
- Generates and saves a summary of the conversation

## Prerequisites

- Python 3.7+
- Streamlit
- OpenAI and Azure OpenAI API keys
- Required Python packages (see below)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/AyushPathak2610/DigiWell.git
    cd DigiWell
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    Create a `.env` file in the root of the project and add your API keys:

    ```plaintext
    OPENAI_API_KEY=your-openai-api-key
    AZURE_API_KEY=your-azure-api-key
    ```

5. Run the Streamlit app:

    ```sh
    streamlit run main.py
    ```

## Usage

- Click "Start Session" to begin the conversation.
- Use the "Start recording" button to record your audio input.
- The bot will respond with both text and audio.
- The conversation history will be displayed.
- Click "End Conversation" to generate and display a summary of the session.

## Project Structure

- `main.py`: Main application code.
- `.env`: Environment variables (not included in the repository).
- `requirements.txt`: List of required Python packages.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [OpenAI](https://www.openai.com/)
- [Azure OpenAI](https://azure.microsoft.com/en-us/services/cognitive-services/openai-service/)
- [pydub](https://github.com/jiaaro/pydub)
- [librosa](https://librosa.org/)
- [soundfile](https://pysoundfile.readthedocs.io/)
- [streamlit-mic-recorder](https://github.com/streamlit/mic-recorder)

## Notes

- Ensure that your API keys are kept secure and not hard-coded into the application.
- The `.env` file should not be included in version control to prevent exposing your API keys.

