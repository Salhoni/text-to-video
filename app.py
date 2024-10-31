# Import necessary libraries
import os
import streamlit as st
import openai
from gtts import gTTS
import cv2
import numpy as np
from PIL import Image
import tempfile

# Set your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'  # Replace with your OpenAI API key

# Define function to generate video from text
def generate_video_from_text(user_input):
    # Step 1: Parse user input
    prompt = f"Generate a short script or storyboard based on the prompt: {user_input}"
    
    # Generate script using OpenAI's API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    script = response['choices'][0]['message']['content']
    print(f"Generated Script: {script}")  # Debugging output

    # Step 2: Generate images based on script (mock-up for demonstration)
    images = []
    for i in range(10):  # Example: Generate 10 frames
        # Here, you can replace this with a call to an image generation model or API
        img = Image.new('RGB', (512, 512), color=(i * 25, i * 25, 255))
        images.append(img)

    # Step 3: Convert images to video
    height, width, layers = np.array(images[0]).shape
    video_name = 'output.avi'
    out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), 1, (width, height))

    for img in images:
        out.write(np.array(img))  # Write image to video
    out.release()

    # Step 4: Generate audio from the script
    tts = gTTS(script, lang='en')
    audio_path = 'audio.mp3'
    tts.save(audio_path)

    return video_name, audio_path

# Streamlit interface
st.title('Text to Video Generator')
user_input = st.text_input("Enter your prompt:")

if st.button('Generate Video'):
    video_path, audio_path = generate_video_from_text(user_input)
    
    # Display generated video
    st.video(video_path)
    
    # Provide a link to download audio
    st.audio(audio_path, format='audio/mp3')

# Optional: Cleanup temporary files after the session
if os.path.exists('output.avi'):
    os.remove('output.avi')
if os.path.exists('audio.mp3'):
    os.remove('audio.mp3')
