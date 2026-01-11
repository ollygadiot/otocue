#!/usr/bin/env python3
"""
Teleprompter Notation to Speech Generator

Converts teleprompter notation to SSML and generates audio using various TTS services.

Supported services:
  - Azure Neural Voices (best prosody support)
  - Google Cloud TTS
  - ElevenLabs

Usage:
  python generate_audio.py --service azure --input structured-script.json --output ./audio/
  python generate_audio.py --service elevenlabs --voice "Adam" --text "Hello **world**"

Environment variables required:
  Azure:      AZURE_SPEECH_KEY, AZURE_SPEECH_REGION
  Google:     GOOGLE_APPLICATION_CREDENTIALS (path to service account JSON)
  ElevenLabs: ELEVENLABS_API_KEY
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

# Load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, rely on environment variables


# =============================================================================
# NOTATION TO SSML CONVERTER
# =============================================================================

def notation_to_ssml(text: str, voice: str = "en-US-DavisNeural") -> str:
    """
    Convert teleprompter notation to SSML.

    Notation reference:
      •           → short pause (300ms)
      • • •       → long pause (1500ms)
      //          → silence/beat (3s)
      **word**    → strong emphasis
      _word_      → soft/understated
      <<text>>    → slow speed
      >>text<<    → fast speed
      ^word^      → pitch up
      ,word,      → pitch down
      WORD        → loud (all caps, 2+ letters)
      ~word~      → whisper
      {style:text}         → speaking style (e.g., {excited:wow!})
      {style,degree:text}  → style with intensity 0.5-2 (e.g., {sad,0.5:oh no})

    Available styles for DavisNeural:
      cheerful, angry, sad, excited, friendly, terrified,
      shouting, whispering, hopeful, empathetic, calm
    """
    result = text

    # Escape XML special characters first (but preserve our notation)
    result = result.replace('&', '&amp;')
    # Don't escape < and > yet - we need them for notation

    # Handle legacy HTML tags - convert to SSML equivalents
    result = re.sub(r'<b>([^<]+)</b>', r'<emphasis level="strong">\1</emphasis>', result)
    result = re.sub(r'<em>([^<]+)</em>', r'<prosody volume="soft">\1</prosody>', result)

    # Speaking styles with degree: {style,degree:text}
    def style_with_degree(match):
        style = match.group(1)
        degree = match.group(2)
        content = match.group(3)
        return f'<mstts:express-as style="{style}" styledegree="{degree}">{content}</mstts:express-as>'

    result = re.sub(r'\{(\w+),(\d+\.?\d*):\s*([^}]+)\}', style_with_degree, result)

    # Speaking styles without degree: {style:text}
    def style_simple(match):
        style = match.group(1)
        content = match.group(2)
        return f'<mstts:express-as style="{style}">{content}</mstts:express-as>'

    result = re.sub(r'\{(\w+):\s*([^}]+)\}', style_simple, result)

    # Silence/beat (//) - must be exact match for standalone
    result = re.sub(r'^//$', '<break time="3s"/>', result)
    result = re.sub(r'(?<!\S)//(?!\S)', '<break time="3s"/>', result)

    # Long pauses (• • •) - must come before short pauses
    result = result.replace('• • •', '<break time="1500ms"/>')

    # Short pauses (•)
    result = result.replace('•', '<break time="300ms"/>')

    # Strong emphasis (**word**)
    result = re.sub(
        r'\*\*([^*]+)\*\*',
        r'<emphasis level="strong">\1</emphasis>',
        result
    )

    # Soft/understated (_word_)
    result = re.sub(
        r'(?<![a-zA-Z])_([^_]+)_(?![a-zA-Z])',
        r'<prosody volume="soft" rate="95%">\1</prosody>',
        result
    )

    # Slow speed (<<text>>)
    result = re.sub(
        r'<<([^<>]+)>>',
        r'<prosody rate="slow">\1</prosody>',
        result
    )

    # Fast speed (>>text<<)
    result = re.sub(
        r'>>([^<>]+)<<',
        r'<prosody rate="fast">\1</prosody>',
        result
    )

    # Pitch up (^word^)
    result = re.sub(
        r'\^([^^]+)\^',
        r'<prosody pitch="+10%">\1</prosody>',
        result
    )

    # Pitch down (,word,) - careful with regular commas
    result = re.sub(
        r',([^,\s][^,]*[^,\s]),',
        r'<prosody pitch="-10%">\1</prosody>',
        result
    )

    # Whisper (~word~)
    result = re.sub(
        r'~([^~]+)~',
        r'<prosody volume="x-soft" rate="90%">\1</prosody>',
        result
    )

    # Loud (ALL CAPS, 2+ letters) - but not inside tags
    def caps_to_loud(match):
        word = match.group(1)
        return f'<prosody volume="loud" rate="90%">{word.capitalize()}</prosody>'

    result = re.sub(r'(?<![<\/\w])(\b[A-Z]{2,}\b)(?![^<]*>)', caps_to_loud, result)

    # Now escape any remaining < > that aren't part of SSML tags
    # (This is tricky - we'll leave as-is since our notation should be converted)

    # Wrap in SSML speak tags (with mstts namespace for styles)
    ssml = f'''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="{voice}">
        {result}
    </voice>
</speak>'''

    return ssml


def notation_to_elevenlabs(text: str) -> str:
    """
    Convert notation to ElevenLabs-compatible format.
    ElevenLabs has limited prosody control, so we approximate.
    """
    result = text

    # Handle legacy HTML tags
    result = re.sub(r'<[^>]+>', '', result)

    # Pauses - ElevenLabs uses ... for pauses
    result = result.replace('• • •', ' ... ... ')
    result = result.replace('•', ' ... ')
    result = re.sub(r'(?<!\S)//(?!\S)', ' ... ... ... ', result)
    result = re.sub(r'^//$', ' ... ... ... ', result)

    # Remove markup that ElevenLabs can't handle (keep the text)
    result = re.sub(r'\*\*([^*]+)\*\*', r'\1', result)
    result = re.sub(r'(?<![a-zA-Z])_([^_]+)_(?![a-zA-Z])', r'\1', result)
    result = re.sub(r'<<([^<>]+)>>', r'\1', result)
    result = re.sub(r'>>([^<>]+)<<', r'\1', result)
    result = re.sub(r'\^([^^]+)\^', r'\1', result)
    result = re.sub(r',([^,\s][^,]*[^,\s]),', r'\1', result)
    result = re.sub(r'~([^~]+)~', r'\1', result)

    # Clean up extra spaces
    result = re.sub(r'\s+', ' ', result).strip()

    return result


# =============================================================================
# TTS SERVICE IMPLEMENTATIONS
# =============================================================================

def generate_azure(ssml: str, output_path: str) -> bool:
    """Generate audio using Azure Neural Voices via REST API."""
    try:
        import requests
    except ImportError:
        print("Error: requests not installed")
        print("Run: pip install requests")
        return False

    speech_key = os.environ.get('AZURE_SPEECH_KEY')
    speech_region = os.environ.get('AZURE_SPEECH_REGION')

    if not speech_key or not speech_region:
        print("Error: Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables")
        return False

    # Get access token
    token_url = f"https://{speech_region}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    token_response = requests.post(token_url, headers={'Ocp-Apim-Subscription-Key': speech_key})

    if token_response.status_code != 200:
        print(f"Failed to get token: {token_response.status_code}")
        print(token_response.text)
        return False

    token = token_response.text

    # Generate speech
    tts_url = f"https://{speech_region}.tts.speech.microsoft.com/cognitiveservices/v1"

    tts_response = requests.post(
        tts_url,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'audio-48khz-192kbitrate-mono-mp3',
            'User-Agent': 'TeleprompterTTS'
        },
        data=ssml.encode('utf-8')
    )

    if tts_response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(tts_response.content)
        return True
    else:
        print(f"TTS error {tts_response.status_code}: {tts_response.text[:500]}")
        return False


def generate_google(ssml: str, output_path: str, voice: str = "en-US-Neural2-F") -> bool:
    """Generate audio using Google Cloud TTS."""
    try:
        from google.cloud import texttospeech
    except ImportError:
        print("Error: google-cloud-texttospeech not installed")
        print("Run: pip install google-cloud-texttospeech")
        return False

    if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        print("Error: Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
        return False

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    voice_params = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0,
        pitch=0.0
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_params,
        audio_config=audio_config
    )

    with open(output_path, 'wb') as f:
        f.write(response.audio_content)

    return True


def generate_elevenlabs(text: str, output_path: str, voice: str = "Adam") -> bool:
    """Generate audio using ElevenLabs API."""
    try:
        import requests
    except ImportError:
        print("Error: requests not installed")
        print("Run: pip install requests")
        return False

    api_key = os.environ.get('ELEVENLABS_API_KEY')
    if not api_key:
        print("Error: Set ELEVENLABS_API_KEY environment variable")
        return False

    # Get voice ID from name
    voice_ids = {
        "adam": "pNInz6obpgDQGcFmaJgB",
        "antoni": "ErXwobaYiN019PkySvjV",
        "arnold": "VR6AewLTigWG4xSOukaG",
        "bella": "EXAVITQu4vr4xnSDxMaL",
        "domi": "AZnzlk1XvdvUeBnXmlld",
        "elli": "MF3mGyEYCl7XYWbV9V6O",
        "josh": "TxGEqnHWrfWFTfGW9XjX",
        "rachel": "21m00Tcm4TlvDq8ikWAM",
        "sam": "yoZ06aMxZJJ28mfd3POQ",
    }

    voice_id = voice_ids.get(voice.lower(), voice)  # Use as ID if not in map

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f"ElevenLabs API error: {response.status_code}")
        print(response.text)
        return False


# =============================================================================
# SCRIPT PROCESSING
# =============================================================================

def load_script(input_path: str) -> dict:
    """Load script from JSON file."""
    with open(input_path, 'r') as f:
        return json.load(f)


def process_script(
    script_data: dict,
    output_dir: str,
    service: str = "azure",
    voice: str = None,
    format: str = "mp3",
    rate_limit: int = 20,
    rate_limit_wait: int = 60
) -> list:
    """
    Process entire script and generate audio files.
    Returns list of generated file paths.

    Args:
        rate_limit: Number of requests before waiting (default 20 for Azure free tier)
        rate_limit_wait: Seconds to wait after hitting rate limit (default 60)
    """
    import time

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    generated_files = []
    segment_num = 0
    request_count = 0

    # Default voices per service
    default_voices = {
        "azure": "en-US-DavisNeural",
        "google": "en-US-Neural2-F",
        "elevenlabs": "Rachel"
    }

    voice = voice or default_voices.get(service, "en-US-DavisNeural")

    for chapter in script_data.get('chapters', []):
        chapter_name = chapter.get('chapter', 'unknown').replace(' ', '_')

        for segment in chapter.get('segments', []):
            segment_num += 1
            line = segment.get('line', '')

            # Skip empty or marker-only lines
            if not line or line in ['[end]', '//']:
                if line == '//':
                    # Generate silence file
                    pass  # Could generate empty audio here
                continue

            # Skip bracketed instructions
            if line.startswith('[') and line.endswith(']'):
                continue

            filename = f"{segment_num:03d}_{chapter_name}.{format}"
            filepath = output_path / filename

            # Skip if file already exists
            if filepath.exists():
                print(f"Skipping {filename} (already exists)")
                generated_files.append(str(filepath))
                continue

            # Rate limiting
            if request_count > 0 and request_count % rate_limit == 0:
                print(f"\n⏳ Rate limit reached. Waiting {rate_limit_wait}s...\n")
                time.sleep(rate_limit_wait)

            print(f"Generating {filename}...")

            success = False
            if service == "azure":
                ssml = notation_to_ssml(line, voice)
                success = generate_azure(ssml, str(filepath))
            elif service == "google":
                ssml = notation_to_ssml(line, voice)
                success = generate_google(ssml, str(filepath), voice)
            elif service == "elevenlabs":
                clean_text = notation_to_elevenlabs(line)
                success = generate_elevenlabs(clean_text, str(filepath), voice)
            else:
                print(f"Unknown service: {service}")
                continue

            request_count += 1

            if success:
                generated_files.append(str(filepath))
                print(f"  ✓ Generated {filepath}")
            else:
                print(f"  ✗ Failed to generate {filepath}")

    return generated_files


def generate_single(
    text: str,
    output_path: str,
    service: str = "azure",
    voice: str = None
) -> bool:
    """Generate audio for a single text string."""

    default_voices = {
        "azure": "en-US-JennyNeural",
        "google": "en-US-Neural2-F",
        "elevenlabs": "Rachel"
    }

    voice = voice or default_voices.get(service)
    success = False

    if service == "azure":
        ssml = notation_to_ssml(text, voice)
        success = generate_azure(ssml, output_path)
    elif service == "google":
        ssml = notation_to_ssml(text, voice)
        success = generate_google(ssml, output_path, voice)
    elif service == "elevenlabs":
        clean_text = notation_to_elevenlabs(text)
        success = generate_elevenlabs(clean_text, output_path, voice)
    else:
        print(f"Unknown service: {service}")
        return False

    if success:
        file_size = os.path.getsize(output_path)
        print(f"Generated {output_path} ({file_size:,} bytes)")

    return success


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Convert teleprompter notation to speech audio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from script file using Azure
  python generate_audio.py --service azure --input structured-script.json --output ./audio/

  # Generate single line with ElevenLabs
  python generate_audio.py --service elevenlabs --voice Rachel --text "Hello **world**" --output hello.mp3

  # Preview SSML conversion (no audio generation)
  python generate_audio.py --preview --text "This is •a **test** •with ^notation^"

Environment variables:
  AZURE_SPEECH_KEY        Azure Speech Services key
  AZURE_SPEECH_REGION     Azure region (e.g., eastus)
  GOOGLE_APPLICATION_CREDENTIALS  Path to Google Cloud service account JSON
  ELEVENLABS_API_KEY      ElevenLabs API key
        """
    )

    parser.add_argument('--service', choices=['azure', 'google', 'elevenlabs'],
                        default='azure', help='TTS service to use')
    parser.add_argument('--input', '-i', help='Input JSON script file')
    parser.add_argument('--output', '-o', help='Output directory or file path')
    parser.add_argument('--text', '-t', help='Single text string to convert')
    parser.add_argument('--voice', '-v', help='Voice name/ID to use')
    parser.add_argument('--preview', action='store_true',
                        help='Preview SSML conversion without generating audio')
    parser.add_argument('--list-voices', action='store_true',
                        help='List available voices for the service')

    args = parser.parse_args()

    # Preview mode - just show SSML
    if args.preview:
        if args.text:
            ssml = notation_to_ssml(args.text)
            print("=== SSML Output ===")
            print(ssml)
            print("\n=== ElevenLabs Output ===")
            print(notation_to_elevenlabs(args.text))
        else:
            print("Error: --text required for preview mode")
            sys.exit(1)
        return

    # List voices
    if args.list_voices:
        print(f"\nRecommended voices for {args.service}:\n")
        if args.service == 'azure':
            print("  en-US-JennyNeural     (female, conversational)")
            print("  en-US-GuyNeural       (male, conversational)")
            print("  en-US-AriaNeural      (female, expressive)")
            print("  en-US-DavisNeural     (male, expressive)")
            print("  en-US-SaraNeural      (female, cheerful)")
            print("\n  Full list: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support")
        elif args.service == 'google':
            print("  en-US-Neural2-F       (female)")
            print("  en-US-Neural2-D       (male)")
            print("  en-US-Studio-O        (female, studio quality)")
            print("  en-US-Studio-M        (male, studio quality)")
            print("\n  Full list: https://cloud.google.com/text-to-speech/docs/voices")
        elif args.service == 'elevenlabs':
            print("  Rachel    (female, calm)")
            print("  Adam      (male, deep)")
            print("  Antoni    (male, warm)")
            print("  Bella     (female, soft)")
            print("  Josh      (male, young)")
            print("  Elli      (female, young)")
            print("\n  Full list: https://elevenlabs.io/voice-library")
        return

    # Single text mode
    if args.text:
        if not args.output:
            print("Error: --output required when using --text")
            sys.exit(1)

        success = generate_single(args.text, args.output, args.service, args.voice)
        sys.exit(0 if success else 1)

    # Script file mode
    if args.input:
        if not args.output:
            args.output = './audio'

        script_data = load_script(args.input)
        files = process_script(script_data, args.output, args.service, args.voice)

        print(f"\n✓ Generated {len(files)} audio files in {args.output}")
        sys.exit(0)

    # No input provided
    parser.print_help()
    sys.exit(1)


if __name__ == '__main__':
    main()
