"""
audio.py
--------
Converts a radio ad script to an audio file using Gemini's native TTS
(gemini-3.1-flash-tts-preview model).
"""

import os
import wave
from google import genai
from google.genai import types

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Saves raw PCM data to a WAV file."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

def generate_audio(script: str, output_path: str) -> None:
    """
    Convert script text to speech using Gemini TTS and save as a .wav file.

    Args:
        script: The radio ad script text.
        output_path: Full path where the .wav will be saved.
    """
    print("🎙️  Converting script to high-quality audio via Gemini TTS...")

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    # Provide clear instructing context natively to the voice act!
    tts_prompt = f"Say the following social media voiceover energetically with viral hype and enthusiasm: {script}"

    response = client.models.generate_content(
        model="gemini-3.1-flash-tts-preview",
        contents=tts_prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Aoede', # Aoede is great for energetic reads
                    )
                )
            ),
        )
    )

    # Extract PCM data
    data = response.candidates[0].content.parts[0].inline_data.data

    # Save to wav
    wave_file(output_path, data)

    print(f"✅  Audio saved to: {output_path}")
