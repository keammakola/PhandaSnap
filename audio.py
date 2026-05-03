"""
audio.py
--------
Converts a radio ad script to audio bytes using Gemini's native TTS.
Refactored to be stateless for serverless deployments (e.g., Vercel).
"""

import os
import wave
import io
from google import genai
from google.genai import types

def generate_audio_bytes(script: str) -> bytes:
    """
    Convert script text to speech bytes using Gemini TTS.
    Returns raw WAV bytes.
    """
    print("🎙️  Converting script to high-quality audio via Gemini TTS (Stateless)...")

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    tts_prompt = f"Say the following social media voiceover energetically with viral hype and enthusiasm: {script}"

    response = client.models.generate_content(
        model="gemini-3.1-flash-tts-preview",
        contents=tts_prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Aoede',
                    )
                )
            ),
        )
    )

    # Extract PCM data
    pcm_data = response.candidates[0].content.parts[0].inline_data.data

    # Convert PCM to WAV in-memory
    with io.BytesIO() as wav_io:
        with wave.open(wav_io, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(pcm_data)
        return wav_io.getvalue()
