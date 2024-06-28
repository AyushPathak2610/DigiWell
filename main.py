import streamlit as st
import os
from openai import AzureOpenAI, OpenAI
from pydub import AudioSegment
import io
from streamlit_mic_recorder import mic_recorder
import base64

# Set API keys
os.environ[
    "OPENAI_API_KEY"] = "sk-proj-FOJlVo80K8SUOMlxkgwLT3BlbkFJ4pyhlya6X7JCvruoSmok"
API_KEY = "394c57a3-013f-4ba5-a763-de1f0f3f7bd9"
ENDPOINT = "https://polite-ground-030dc3103.4.azurestaticapps.net/api/v1"
API_VERSION = "2024-02-01"
MODEL_NAME = "gpt-35-turbo"

openai_client = OpenAI()

azure_client = AzureOpenAI(
    azure_endpoint=ENDPOINT,
    api_key=API_KEY,
    api_version=API_VERSION,
)

# System prompt to set the context
system_prompt = """
You are a mental health counselor. Your role is to engage in a therapeutic session with me, similar to how a psychologist or counselor would. Initiate the conversation and encourage me to express my emotions in detail. Provide solutions to my concerns and, if asked, offer diagnoses and treatment options. This can be a long session, so feel free to delve into greater detail and explore various aspects of my mental health.
"""

# Initialize session state variables
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "audio_counter" not in st.session_state:
    st.session_state.audio_counter = 0


def generate_response(user_input=None, audio_bytes=None):
    # Transcribe the audio bytes if provided
    if audio_bytes:
        temp_audio_path = "input_audio.mp3"
        audio_bytes_io = io.BytesIO(audio_bytes)
        audio_segment = AudioSegment.from_file(audio_bytes_io)
        audio_segment.export(temp_audio_path, format="mp3")

        with open(temp_audio_path, "rb") as audio_file:
            transcription = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en",
                temperature=0.2)
            user_input = transcription.text.strip()

    # Add initial greeting if the conversation is just starting
    if not st.session_state.conversation_history and user_input is None:
        initial_greeting = "Hello, I'm here to help you. How have you been feeling lately?"
        st.session_state.conversation_history.append({
            "role":
            "assistant",
            "content":
            initial_greeting
        })
        audio_url = create_audio_response(initial_greeting)
        return initial_greeting, audio_url

    # Update conversation history with the new user input
    if user_input:
        st.session_state.conversation_history.append({
            "role": "user",
            "content": user_input
        })

    # Prepare the messages for the API call
    messages = [{
        "role": "system",
        "content": system_prompt
    }] + st.session_state.conversation_history

    # Create a chat completion
    chat_completion = azure_client.chat.completions.create(
        messages=messages,
        model=MODEL_NAME,
        max_tokens=1000,
        temperature=0.3,
    )

    # Extract the bot's response
    bot_response = chat_completion.choices[0].message.content.strip()

    # Update conversation history with the bot's response
    st.session_state.conversation_history.append({
        "role": "assistant",
        "content": bot_response
    })

    # Create audio response
    audio_url = create_audio_response(bot_response)

    return bot_response, audio_url


def create_audio_response(input_text):
    response = openai_client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text,
    )
    response.stream_to_file("bot_output.mp3")
    audio_file = open("bot_output.mp3", "rb")
    audio_bytes = audio_file.read()
    audio_b64 = base64.b64encode(audio_bytes).decode()
    audio_url = f"data:audio/mp3;base64,{audio_b64}"
    return audio_url


def get_gif_as_base64(gif_path):
    with open(gif_path, "rb") as gif_file:
        gif_bytes = gif_file.read()
    gif_b64 = base64.b64encode(gif_bytes).decode()
    return gif_b64


gif_base64 = get_gif_as_base64("audio.gif")


def play_audio(audio_url):
    audio_html = f"""
    <audio src="{audio_url}" controls autoplay>
        Your browser does not support the audio element.
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)


def generate_summary(conversation_history):
    summary_prompt = "Please summarize the following conversation history:\n\n"
    for message in conversation_history:
        role = "User" if message["role"] == "user" else "Bot"
        summary_prompt += f"{role}: {message['content']}\n"
    summary_prompt += "\nSummary:"

    # Use azure_client for generating summary
    summary_completion = azure_client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": summary_prompt
        }],
        model=MODEL_NAME,
        max_tokens=200,
        temperature=0.5,
    )
    summary = summary_completion.choices[0].message.content.strip()
    return summary


def save_summary(summary):
    with open("conversation_summary.txt", "w") as file:
        file.write(summary)


def get_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string


# Streamlit app
if 'record' not in st.session_state:
    st.session_state.record = False

if 'session' not in st.session_state:
    st.session_state.session = False

if 'session_end' not in st.session_state:
    st.session_state.session_end = False

if 'session_start' not in st.session_state:
    st.session_state.session_start = True

st.title("Mental Health Chatbot")

# Add custom CSS for styling and icons
st.markdown("""
    <style>
        .stApp {
            background-color: rgba(33,33,33,255);
        }
        .user-message, .bot-message {
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            color:white
        }
        .user-message {
            background-color: #0d0d0d;
            text-align: left;
        }
        .bot-message {
            background-color: #2f2f2f;
            text-align: left;
        }
        .message-container {
            display: flex;
            align-items: flex-start;
            margin-bottom: 10px;
        }
        .message-icon {
            width: 40px;
            height: 40px;
            margin-right: 10px;
        }
        .stButton {
            color: white;
            border: none;
            border-radius: 4px;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            cursor: pointer;
        }
       
           
                .stApp {
                    background-color: rgba(33,33,33,255);
                    border: 2px solid #555;
                    border-radius: 10px;
                    padding: 20px;
                    width: 80vw;
                    margin: 20px auto; /* Center align and add space around */   
                    margin-top:4rem;
                }
                .stButton {
                    color: white;
                    border: none;
                    border-radius: 4px;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    cursor: pointer;
                    margin-top: 10px; /* Increase vertical gap */
                    margin-bottom: 10px; /* Increase vertical gap */
                }

                .navbar {
                    background-color: #333;
                    padding: 10px 0;
                    text-align: center;
                    margin-bottom: 20px;
                    border-bottom: 2px solid #555;
                }
                .navbar-title {
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                }


    </style>
""",
            unsafe_allow_html=True)


def main():
    st.markdown("""
        <style>
            .record-button {
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 10px;
            }
            .record-button:hover {
                background-color: #45a049;
            }
        </style>
    """,
                unsafe_allow_html=True)

    if st.session_state.session_start:
        if st.button("Start Session"):
            greeting, audio_url = generate_response()
            play_audio(audio_url)
            st.session_state.record = True
            st.session_state.session = True
            st.session_state.session_start = False
            # st.experimental_rerun()

    # Path to your PNG icon file
    icon_path = "record.png"

    # Display summary
    if st.session_state.session:
        # Record audio
        if st.session_state.record:
            voice_recording = mic_recorder(
                start_prompt="🎙️ Start recording",
                stop_prompt="🛑 Stop recording",
                just_once=False,
                use_container_width=True,
            )

            if voice_recording is not None:
                audio_bytes = voice_recording['bytes']
                response, audio_url = generate_response(
                    audio_bytes=audio_bytes)
                play_audio(audio_url)

        if st.button("End Conversation"):
            st.session_state.session_end = True
            st.session_state.session = False
            st.experimental_rerun()

        # Display conversation
        st.subheader("Conversation History")

        user_icon_b64 = get_image_as_base64("user-icon.png")
        bot_icon_b64 = get_image_as_base64("bot-icon.png")

        for message in st.session_state.conversation_history:
            role = "User" if message["role"] == "user" else "Bot"
            icon = user_icon_b64 if role == "User" else bot_icon_b64
            message_class = "user-message" if role == "User" else "bot-message"
            st.markdown(f"""
                <div class="message-container">
                    <img src="data:image/png;base64,{icon}" class="message-icon">
                    <div class="{message_class}">
                        <strong>{role}:</strong> {message['content']}
                    </div>
                </div>
            """,
                        unsafe_allow_html=True)

    if st.session_state.session_end:
        summary = generate_summary(st.session_state.conversation_history)
        st.write("Summary:")
        st.write(summary)
        save_summary(summary)
        st.write("Conversation ended. Thank you!")


if __name__ == '__main__':
    main()
