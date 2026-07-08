"""
audio.py
--------
Converts a script to audio bytes using Gemini's native TTS.
Contains a robust fallback to generate a silent WAV if the API call fails.
"""

import os
import wave
import io
from google import genai
from google.genai import types

def generate_audio_bytes(script: str) -> bytes:
    """
    Convert script text to speech bytes using Gemini TTS.
    Returns raw WAV bytes. Falls back to silent WAV on failure.
    """
    # ponytail: return simple mock/silent WAV if API key is missing
    if not os.environ.get("GEMINI_API_KEY"):
        print("[WARNING] GEMINI_API_KEY not found. Generating fallback WAV.")
        return generate_fallback_wav()

    try:
        print("🎙️  Converting script to high-quality audio via Gemini TTS...")
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
        # The GenAI response may contain audio in different fields depending on SDK version.
        # Try a few known shapes: candidates[].content.parts[].inline_data.data, response.output_audio,
        # or a base64-encoded text payload in response.text.
        pcm_data = None
        try:
            # Try the candidates -> inline_data path first
            pcm_data = response.candidates[0].content.parts[0].inline_data.data
            print("[INFO] Extracted audio from candidates.inline_data")
        except Exception:
            pcm_data = None

        if not pcm_data:
            # Some SDKs expose the binary audio on response.output_audio or similar
            try:
                pcm_data = getattr(response, "output_audio", None)
                if pcm_data:
                    print("[INFO] Extracted audio from response.output_audio")
            except Exception:
                pcm_data = None

        if not pcm_data:
            # As a last resort, try to treat response.text as base64-encoded audio
            try:
                import base64
                txt = (response.text or "").strip()
                if txt:
                    decoded = base64.b64decode(txt)
                    if len(decoded) > 800:  # basic sanity check
                        pcm_data = decoded
                        print("[INFO] Decoded audio from response.text base64")
            except Exception:
                pcm_data = None

        if not pcm_data:
            raise RuntimeError("No audio payload found in Gemini response")

        # If pcm_data is a bytes-like PCM stream, wrap into a WAV container
        with io.BytesIO() as wav_io:
            with wave.open(wav_io, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                # Some responses are 24000Hz, others 16000; try 24000 first, if playback weird adjust later
                wf.setframerate(24000)
                # If provided pcm_data is str (decoded base64), ensure bytes
                if isinstance(pcm_data, str):
                    pcm_data = pcm_data.encode('latin1')
                wf.writeframes(pcm_data)
            return wav_io.getvalue()
    except Exception as e:
        print(f"[WARNING] Gemini TTS failed: {e}. Generating fallback WAV.")
        return generate_fallback_wav()

def generate_audio(script: str, output_path: str) -> None:
    """
    Convert script text to speech and save as a WAV file.
    """
    audio_bytes = generate_audio_bytes(script)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)

def generate_fallback_wav() -> bytes:
    """
    Generates a tiny valid 1-second silent WAV file.
    """
    # ponytail: generate silent WAV using built-in wave module (no dependencies)
    with io.BytesIO() as wav_io:
        with wave.open(wav_io, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(8000)
            wf.writeframes(b'\x00' * 16000) # 1 second of silence
        return wav_io.getvalue()
