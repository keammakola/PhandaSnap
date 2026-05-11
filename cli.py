"""
main.py
-------
Interactive CLI entry point for the Hustle Engine Radio Ad Generator.
Collects store details and discount promos, generates a Gemini-powered
South African radio ad script, and exports both .txt and .mp3 outputs.
"""

import os
import re
from pathlib import Path
from generator import generate_script
from audio import generate_audio
from image import generate_poster

OUTPUT_DIR = Path("outputs")


def slugify(text: str) -> str:
    """Convert a store name to a safe filename slug."""
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def print_banner():
    print()
    print("=" * 60)
    print("  📱   HUSTLE ENGINE — Social Media Toolkit")
    print("  Powered by Gemini AI  |  Made for Viral Engagement")
    print("=" * 60)
    print()


def collect_inputs() -> tuple[str, str, list[str], str]:
    """Prompt the user for all ad generation inputs."""

    store_name = input("📌  Store name: ").strip()
    while not store_name:
        print("   ⚠️  Store name cannot be empty.")
        store_name = input("📌  Store name: ").strip()

    promo_end = input("📅  Promo end date (e.g. 30 April 2025): ").strip()
    while not promo_end:
        print("   ⚠️  Promo end date cannot be empty.")
        promo_end = input("📅  Promo end date: ").strip()

    language = input("🗣️   Language (e.g. English, Zulu, Afrikaans) [default: English]: ").strip()
    if not language:
        language = "English"

    print()
    print("🛍️   Enter each promo deal on its own line.")
    print("     Press ENTER on an empty line when you're done.\n")

    promos = []
    i = 1
    while True:
        deal = input(f"   Deal {i}: ").strip()
        if not deal:
            if not promos:
                print("   ⚠️  Add at least one deal before continuing.")
                continue
            break
        promos.append(deal)
        i += 1

    return store_name, promo_end, promos, language


def save_caption(caption: str, store_slug: str) -> Path:
    """Save the generated caption to a .txt file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / f"{store_slug}_caption.txt"
    path.write_text(caption, encoding="utf-8")
    print(f"💬  Caption saved to: {path}")
    return path


def main():
    print_banner()

    store_name, promo_end, promos, language = collect_inputs()
    slug = slugify(store_name)

    # Generate caption and voiceover
    caption, voiceover = generate_script(store_name, promo_end, promos, language)

    # Display caption in terminal
    print()
    print("─" * 60)
    print("💬  YOUR SOCIAL MEDIA CAPTION:")
    print("─" * 60)
    print(caption)
    print("─" * 60)
    print()

    # Save outputs
    OUTPUT_DIR.mkdir(exist_ok=True)
    save_caption(caption, slug)

    audio_path = OUTPUT_DIR / f"{slug}_voiceover.wav"
    generate_audio(voiceover, str(audio_path))
    
    poster_path = OUTPUT_DIR / f"{slug}_social_graphic.jpg"
    generate_poster(store_name, promos, str(poster_path))

    print()
    print("🎉  All done! Your asset bundle is ready.")
    print(f"    💬  Caption   : outputs/{slug}_caption.txt")
    print(f"    🔊  Voiceover : outputs/{slug}_voiceover.wav")
    print(f"    🎨  Graphic   : outputs/{slug}_social_graphic.jpg")
    print()


if __name__ == "__main__":
    main()
