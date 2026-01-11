# Voice Generation Guide

Convert teleprompter notation to natural speech with proper pacing, emphasis, and emotional delivery.

## Quick Start

```bash
# Install dependencies
pip install -r requirements-tts.txt

# Set up credentials (Azure example)
export AZURE_SPEECH_KEY="your-key"
export AZURE_SPEECH_REGION="eastus"

# Generate audio from script
python generate_audio.py --service azure --input structured-script.json --output ./audio/
```

---

## Supported Services

| Service | Prosody Control | Cost | Best For |
|---------|-----------------|------|----------|
| **Azure Neural Voices** | Excellent | ~$16/1M chars | Full notation support |
| **Google Cloud TTS** | Good | ~$16/1M chars | Good alternative |
| **ElevenLabs** | Limited | ~$0.30/1K chars | Natural voice quality |

### Recommendation

**Azure Neural Voices** provides the best match for our notation system. It fully supports SSML prosody tags for rate, pitch, volume, emphasis, and breaks.

---

## Installation

```bash
pip install -r requirements-tts.txt
```

Or install individually:

```bash
# Azure
pip install azure-cognitiveservices-speech

# Google Cloud
pip install google-cloud-texttospeech

# ElevenLabs
pip install requests
```

---

## Configuration

### Azure Neural Voices

1. Create an Azure Speech Services resource at [portal.azure.com](https://portal.azure.com)
2. Copy your key and region
3. Set environment variables:

```bash
export AZURE_SPEECH_KEY="your-key-here"
export AZURE_SPEECH_REGION="eastus"  # or your region
```

### Google Cloud TTS

1. Create a project at [console.cloud.google.com](https://console.cloud.google.com)
2. Enable the Text-to-Speech API
3. Create a service account and download JSON key
4. Set environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```

### ElevenLabs

1. Sign up at [elevenlabs.io](https://elevenlabs.io)
2. Get your API key from profile settings
3. Set environment variable:

```bash
export ELEVENLABS_API_KEY="your-api-key"
```

---

## Usage

### Preview SSML Conversion

See how notation converts to SSML without generating audio:

```bash
python generate_audio.py --preview --text "This is •a **test** • • •with ^notation^"
```

Output:
```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="en-US-JennyNeural">
        This is <break time="300ms"/>a <emphasis level="strong">test</emphasis>
        <break time="1500ms"/>with <prosody pitch="+10%">notation</prosody>
    </voice>
</speak>
```

### Generate Single Line

```bash
# Azure
python generate_audio.py --service azure --text "They're getting ,**BUILT**,." -o test.mp3

# With specific voice
python generate_audio.py --service azure --voice en-US-GuyNeural --text "Hello **world**" -o hello.mp3

# ElevenLabs
python generate_audio.py --service elevenlabs --voice Rachel --text "Hello world" -o hello.mp3
```

### Generate Entire Script

```bash
# From JSON script file
python generate_audio.py --service azure --input structured-script.json --output ./audio/

# With custom voice
python generate_audio.py --service azure --voice en-US-DavisNeural --input structured-script.json --output ./audio/
```

### List Available Voices

```bash
python generate_audio.py --service azure --list-voices
python generate_audio.py --service google --list-voices
python generate_audio.py --service elevenlabs --list-voices
```

---

## Notation Reference

### Pauses

| Notation | SSML Output | Duration | Use For |
|----------|-------------|----------|---------|
| `•` | `<break time="300ms"/>` | 0.3s | Breath, rhythm between clauses |
| `• • •` | `<break time="1500ms"/>` | 1.5s | Dramatic pause, letting ideas land |
| `//` | `<break time="3s"/>` | 3s | Complete silence, major beat |

### Emphasis

| Notation | SSML Output | Effect | Use For |
|----------|-------------|--------|---------|
| `**word**` | `<emphasis level="strong">` | Stressed, prominent | Key concepts, emotional peaks |
| `_word_` | `<prosody volume="soft" rate="95%">` | Softer, slower | Asides, vulnerability, trailing off |

### Speed

| Notation | SSML Output | Effect | Use For |
|----------|-------------|--------|---------|
| `<<text>>` | `<prosody rate="slow">` | Slower delivery | Important realizations, weight |
| `>>text<<` | `<prosody rate="fast">` | Faster delivery | Lists, building energy, montages |

### Pitch

| Notation | SSML Output | Effect | Use For |
|----------|-------------|--------|---------|
| `^word^` | `<prosody pitch="+10%">` | Higher pitch | Questions, curiosity, anticipation |
| `,word,` | `<prosody pitch="-10%">` | Lower pitch | Finality, gravity, conclusions |

### Volume

| Notation | SSML Output | Effect | Use For |
|----------|-------------|--------|---------|
| `WORD` | `<prosody volume="loud" rate="90%">` | Louder, punchy | Impact moments, breakthroughs |
| `~word~` | `<prosody volume="x-soft" rate="90%">` | Whisper | Vulnerability, intimacy, secrets |

---

## Conversion Examples

### Example 1: Emotional Admission

**Input:**
```
And as a maker, •<<not being able to build your ideas>> is... • • •~pretty tough~.
```

**SSML Output:**
```xml
And as a maker, <break time="300ms"/>
<prosody rate="slow">not being able to build your ideas</prosody> is...
<break time="1500ms"/>
<prosody volume="x-soft" rate="90%">pretty tough</prosody>.
```

**Why it works:**
- Breath before the painful clause
- Slow down to give weight to the problem
- Long pause for emotional impact
- Whisper the vulnerable admission

### Example 2: Question with Rising Pitch

**Input:**
```
^Could this closet be the key^ •to finally building all the projects?
```

**SSML Output:**
```xml
<prosody pitch="+10%">Could this closet be the key</prosody>
<break time="300ms"/>to finally building all the projects?
```

### Example 3: Powerful Single Word

**Input:**
```
,**Gone**,.
```

**SSML Output:**
```xml
<prosody pitch="-10%"><emphasis level="strong">Gone</emphasis></prosody>.
```

**Why it works:**
- Pitch drops for finality
- Strong emphasis for impact
- Single word = maximum power

---

## Recommended Voices

### Azure Neural Voices

| Voice | Gender | Style | Best For |
|-------|--------|-------|----------|
| `en-US-JennyNeural` | Female | Conversational | General narration |
| `en-US-GuyNeural` | Male | Conversational | General narration |
| `en-US-AriaNeural` | Female | Expressive | Emotional content |
| `en-US-DavisNeural` | Male | Expressive | Emotional content |
| `en-US-SaraNeural` | Female | Cheerful | Upbeat content |

[Full list →](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support)

### Google Cloud TTS

| Voice | Gender | Quality |
|-------|--------|---------|
| `en-US-Neural2-F` | Female | Neural |
| `en-US-Neural2-D` | Male | Neural |
| `en-US-Studio-O` | Female | Studio (highest quality) |
| `en-US-Studio-M` | Male | Studio (highest quality) |

[Full list →](https://cloud.google.com/text-to-speech/docs/voices)

### ElevenLabs

| Voice | Gender | Character |
|-------|--------|-----------|
| `Rachel` | Female | Calm, clear |
| `Adam` | Male | Deep, authoritative |
| `Antoni` | Male | Warm, friendly |
| `Bella` | Female | Soft, gentle |
| `Josh` | Male | Young, energetic |

[Full list →](https://elevenlabs.io/voice-library)

---

## Output Files

When processing a full script, files are named:

```
./audio/
├── 001_The_Pipe_Dream_Drawer.mp3
├── 002_The_Pipe_Dream_Drawer.mp3
├── 003_The_Pipe_Dream_Drawer.mp3
├── 004_The_50ft²_Bet.mp3
└── ...
```

Format: `{segment_number}_{chapter_name}.mp3`

---

## ElevenLabs Limitations

ElevenLabs doesn't support full SSML, so the script approximates:

| Notation | ElevenLabs Conversion |
|----------|----------------------|
| `•` | `...` (pause) |
| `• • •` | `... ...` (longer pause) |
| `**word**` | `word` (markup stripped) |
| Other markup | Stripped, text preserved |

For best prosody control, use **Azure** or **Google Cloud**.

---

## Troubleshooting

### Azure: "Invalid subscription key"
- Check `AZURE_SPEECH_KEY` is set correctly
- Verify the key is active in Azure portal
- Ensure `AZURE_SPEECH_REGION` matches your resource's region

### Google: "Could not automatically determine credentials"
- Verify `GOOGLE_APPLICATION_CREDENTIALS` points to valid JSON file
- Ensure the service account has Text-to-Speech API access

### ElevenLabs: "401 Unauthorized"
- Check `ELEVENLABS_API_KEY` is set
- Verify your API key is valid and has remaining quota

### General: No audio generated
- Run with `--preview` first to check SSML output
- Check for malformed notation in your script
- Ensure output directory exists and is writable

---

## Programmatic Usage

```python
from generate_audio import notation_to_ssml, generate_azure

# Convert notation to SSML
text = "This is •a **test** with ^notation^"
ssml = notation_to_ssml(text, voice="en-US-JennyNeural")

# Generate audio
generate_azure(ssml, "output.mp3")
```

---

## Cost Estimation

For a 5-minute video script (~3,000 characters):

| Service | Estimated Cost |
|---------|----------------|
| Azure | ~$0.05 |
| Google Cloud | ~$0.05 |
| ElevenLabs | ~$0.90 |

*Prices as of 2024. Check provider websites for current pricing.*
