# Otocue

**Stop reading scripts. Start performing them.**

Otocue is a rich teleprompter app built for creators who want to nail their delivery every single time. It's not just about reading words — it's about knowing _when to pause_, _what to punch_, and _how to land every line_.

Your script becomes a performance guide: pauses appear as visual breaks, key words glow, whispers fade, and emphasis jumps off the screen. You'll never wonder "how should I say this?" again.

Once you try it, you won't go back to a blank teleprompter.

## Why Otocue?

- **Delivery baked into the script** — See exactly where to pause, what to emphasize, when to slow down
- **Hand gesture cues** — Visual reminders for body language alongside your script
- **Three modes for any workflow** — Smooth scroll, auto-advance, or one segment at a time
- **Works on any device** — Phone, tablet, laptop. No app install needed
- **Script library** — Save multiple scripts locally, switch between them anytime
- **iPad mode** — Tap anywhere to advance. Perfect next to your camera
- **Generate voice previews** — Hear how your script sounds with AI voices before you record
- **LLM-powered script prep** — Paste your draft, get back a performance-ready script with all the cues

## Quick Start

1. Open `otocue.html` in a web browser
2. Upload your script JSON file (drag & drop or click to browse)
3. Your script is saved in localStorage — it persists between sessions
4. Use the controls at the top (hover to reveal) or keyboard shortcuts

To load a different script, click "Load Script" in the top controls.

### Keyboard Shortcuts

| Key       | Action                              |
| --------- | ----------------------------------- |
| `Space`   | Play/Pause (or Next in Static mode) |
| `↑` / `↓` | Previous/Next segment               |
| `←` / `→` | Decrease/Increase speed             |
| `R`       | Reset to beginning                  |
| `L`       | Toggle legend panel                 |
| `G`       | Toggle gesture display              |

## Display Modes

### Scroll Mode

Continuously scrolls through the script at adjustable speed. Good for traditional teleprompter use.

### Auto Mode

Advances segment-by-segment with timing based on word count. Adjusts reading speed with the slider.

### Static Mode

Shows one segment at a time. Press Space or tap (in iPad mode) to advance. Best for memorization practice.

## Script Format

Scripts use a JSON structure with chapters and segments:

```json
{
  "title": "My Video Script",
  "chapters": [
    {
      "chapter": "Introduction",
      "timestamp": "0:00",
      "segments": [
        {
          "line": "Your script text with **notation** goes here.",
          "format": "on-camera",
          "notes": "Optional production notes"
        }
      ]
    }
  ]
}
```

### Segment Properties

| Property    | Description                                                               |
| ----------- | ------------------------------------------------------------------------- |
| `line`      | The script text with notation markup                                      |
| `format`    | Either `"on-camera"` (white text) or `"b-roll"` (gold text for voiceover) |
| `notes`     | Optional production/direction notes (toggle visibility with checkbox)     |
| `gesture`   | Optional hand/arm gesture cue (see [Gestures](#gestures) section)         |
| `reasoning` | Optional explanation for format choice (not displayed)                    |

## Notation Reference

### Pauses

| Notation | Display          | Duration | Use For                            |
| -------- | ---------------- | -------- | ---------------------------------- |
| `•`      | Short break      | 300ms    | Breath between clauses             |
| `• • •`  | Breathing circle | 1500ms   | Dramatic pause, letting ideas land |
| `//`     | Silence marker   | 3s       | Complete beat, eye contact moment  |

### Emphasis

| Notation        | Display                  | Use For                             |
| --------------- | ------------------------ | ----------------------------------- |
| `**word**`      | Glowing strong text      | Key concepts, emotional peaks       |
| `_word_`        | Soft, faded text         | Asides, trailing off, vulnerability |
| `<b>word</b>`   | Bold (legacy)            | Same as `**word**`                  |
| `<em>word</em>` | Reduced opacity (legacy) | Same as `_word_`                    |

### Speed

| Notation   | Display              | Use For                          |
| ---------- | -------------------- | -------------------------------- |
| `<<text>>` | Wider letter spacing | Important realizations, weight   |
| `>>text<<` | Tighter spacing      | Lists, building energy, montages |

### Pitch

| Notation | Display             | Use For                            |
| -------- | ------------------- | ---------------------------------- |
| `^word^` | Raised, blue-tinted | Questions, curiosity, anticipation |
| `,word,` | Lowered, gray       | Finality, conclusions, gravity     |

### Volume

| Notation | Display      | Use For                                   |
| -------- | ------------ | ----------------------------------------- |
| `WORD`   | Large, bold  | Impact moments (use sparingly, 1-2 words) |
| `~word~` | Small, faded | Whisper, vulnerability, secrets           |

### Emotional Styles

For TTS generation with Azure DavisNeural voice:

| Notation             | Effect            |
| -------------------- | ----------------- |
| `{excited: text}`    | High energy       |
| `{cheerful: text}`   | Happy, upbeat     |
| `{sad: text}`        | Melancholy        |
| `{hopeful: text}`    | Optimistic        |
| `{empathetic: text}` | Understanding     |
| `{calm: text}`       | Relaxed, soothing |
| `{angry: text}`      | Frustration       |
| `{friendly: text}`   | Warm              |
| `{terrified: text}`  | Fear              |
| `{shouting: text}`   | Loud exclamation  |
| `{whispering: text}` | Intimate          |

Intensity can be specified: `{sad,0.5: text}` (range 0.5-2)

## Gestures

Otocue can display hand and arm gesture cues alongside your script to guide body language during delivery. Research shows effective speakers use nearly twice as many hand gestures as less engaging speakers.

### Enabling Gestures

- Check the "Gestures" checkbox in the control bar, or press `G`
- Gesture icons appear in the top-right corner of segments that have them
- Hover over a gesture to see its name

### Adding Gestures to Your Script

Add a `gesture` property to any segment:

```json
{
  "line": "Welcome to my presentation.",
  "format": "on-camera",
  "gesture": "arms-open"
}
```

### Available Gestures

#### Presentation Essentials

| Gesture ID      | Description                                    | Use For                                    |
| --------------- | ---------------------------------------------- | ------------------------------------------ |
| `palm-up`       | Open palm facing up                            | Honesty, welcoming, questions              |
| `palm-down`     | Palm facing down                               | Calming, authoritative statements          |
| `open-hands`    | Both palms visible                             | Maximum trust, openings, conclusions       |
| `measure-loaf`  | Hands apart, palms facing                      | Showing scope, framing content             |

#### Emphasis & Pointing

| Gesture ID        | Description                                  | Use For                                    |
| ----------------- | -------------------------------------------- | ------------------------------------------ |
| `pinching`        | Thumb and finger pinched                     | Precision, key details                     |
| `point-at-viewer` | Index finger forward                         | Direct address, calls to action            |
| `index-up`        | Fist with thumb up (Clinton thumb)           | Emphasis without accusation                |
| `thumbs-up`       | Approval gesture                             | Positive reinforcement, agreement          |

#### Counting & Lists

| Gesture ID     | Description                                     | Use For                                    |
| -------------- | ----------------------------------------------- | ------------------------------------------ |
| `countdown-1`  | One finger raised                               | First item                                 |
| `countdown-2`  | Two fingers (peace sign)                        | Second item                                |
| `countdown-3`  | Three fingers                                   | Third item                                 |
| `countdown-4`  | Four fingers                                    | Fourth item                                |
| `countdown-5`  | Full hand                                       | Fifth item                                 |
| `compare`      | Two hands in different positions                | Comparing options, pros/cons               |

#### Emotional Connection

| Gesture ID      | Description                                    | Use For                                    |
| --------------- | ---------------------------------------------- | ------------------------------------------ |
| `heart-touch`   | Hand over heart                                | Sincerity, personal stories                |
| `folded-hands`  | Hands together                                 | Gratitude, requests                        |
| `expand-clasp`  | Hands coming together                          | Unity, bringing ideas together             |
| `raising-hands` | Both hands raised                              | Celebration, excitement                    |

#### Body & Arms

| Gesture ID     | Description                                     | Use For                                    |
| -------------- | ----------------------------------------------- | ------------------------------------------ |
| `arms-open`    | Arms spread wide                                | Big moments, welcoming                     |
| `arms-sides`   | Neutral position                                | Pauses, listening, reset                   |
| `flexed-biceps`| Flexed arm                                      | Strength, determination                    |

#### Avoid These

| Gesture ID      | Description                                    | Why to Avoid                               |
| --------------- | ---------------------------------------------- | ------------------------------------------ |
| `arms-crossed`  | Crossed arms (shown with red X)                | Signals defensiveness, reduces retention   |

### Running Locally

**Note**: Gestures require loading from a web server due to browser security. Use:

```bash
cd otocue
python3 -m http.server 8080
# Then open http://localhost:8080/otocue.html
```

## Example Script

```json
{
  "title": "Demo",
  "chapters": [
    {
      "chapter": "Opening",
      "timestamp": "0:00",
      "segments": [
        {
          "line": "For **years** I thought I needed more space.",
          "format": "on-camera",
          "notes": null
        },
        {
          "line": "But then •everything changed. • • •",
          "format": "on-camera",
          "notes": "pause for effect"
        },
        {
          "line": "^Could this tiny room be enough?^",
          "format": "on-camera",
          "notes": null
        },
        {
          "line": "//",
          "format": "on-camera",
          "notes": "hold eye contact"
        },
        {
          "line": ",**Yes**,.",
          "format": "on-camera",
          "notes": "deliver with conviction"
        }
      ]
    }
  ]
}
```

## Audio Generation

Otocue can generate TTS audio for each segment. See [VOICE_GENERATION.md](VOICE_GENERATION.md) for setup instructions.

### Quick Start

```bash
# Install dependencies
pip install requests python-dotenv

# Set credentials
export AZURE_SPEECH_KEY="your-key"
export AZURE_SPEECH_REGION="eastus"

# Generate audio
python generate_audio.py --service azure --input example-script.json --output ./audio/
```

### Supported Services

| Service             | Prosody Support | Best For              |
| ------------------- | --------------- | --------------------- |
| Azure Neural Voices | Excellent       | Full notation support |
| Google Cloud TTS    | Good            | Alternative option    |
| ElevenLabs          | Limited         | Natural voice quality |

### Preview SSML

Test notation conversion without generating audio:

```bash
python generate_audio.py --preview --text "This is •a **test** with ^notation^"
```

## Loading Scripts

1. Open `otocue.html` in your browser
2. Drag & drop your JSON file onto the upload area, or click to browse
3. Your script loads immediately and is saved to your library

**Script library**: All uploaded scripts are saved locally. Click "Load Script" in the control bar to switch between scripts or upload new ones.

**Privacy**: Your scripts never leave your device. Everything is stored locally in your browser.

## Creating Scripts with an LLM

The easiest way to create a structured script is to provide your plain text to an LLM (like Claude, ChatGPT, or similar) and have it generate the JSON with delivery notation.

### Recommended Workflow

1. **Write your script** as plain text, focusing on the content
2. **Provide it to an LLM** with the notation reference and JSON format
3. **Review and refine** the generated output

### Example Prompt

Paste the contents of [`NOTATION_GUIDE.md`](NOTATION_GUIDE.md) into your LLM conversation, then add:

```
Convert the following script to Otocue JSON format using the notation above.
Decide for each segment whether it should be "on-camera" or "b-roll".
Add production notes where helpful.

[paste your plain text script here]
```

### Tips

- **Provide context** about the video's tone and audience
- **Share examples** from `example-script.json` for reference
- **Iterate** - ask the LLM to adjust specific sections if the notation feels off

## Writing Effective Scripts

### Principles

1. **Less is more** - Don't mark every word. Reserve notation for moments that matter.

2. **Contrast creates meaning** - Slow sections need fast sections. Whispers need loud moments.

3. **Pauses are punctuation** - Use `•` like commas, `• • •` like periods, `//` like paragraph breaks.

4. **Match content to form**:

   - Questions → `^pitch up^`
   - Answers → `,pitch down,`
   - Lists → `>>speed up<<`
   - Insights → `<<slow down>>`
   - Pain → `~whisper~`
   - Triumph → `**LOUD**`

5. **Serve the story** - Every notation should help deliver emotional truth.

### Conversion Example

**Plain text:**

```
I never thought it would work. But then everything changed.
```

**With notation:**

```
I _never_ thought it would work. • • •But then •<<**everything** changed>>.
```

**Why:**

- Soft emphasis on "never" for self-doubt (`_..._`)
- Long pause before the pivot (`• • •`)
- Short breath before the revelation (`•`)
- Slow down and emphasize the key moment (`<<**...**>>`)

## File Structure

```
otocue/
├── otocue.html           # Main application
├── generate_audio.py     # TTS audio generator
├── example-script.json   # Example script with gesture examples
├── NOTATION_GUIDE.md     # LLM prompt reference for script conversion
├── VOICE_GENERATION.md   # TTS setup guide
├── README.md             # This file
├── gestures/             # Gesture icon library
│   ├── gestures.json     # Gesture metadata and descriptions
│   ├── palm-up.svg       # Individual gesture icons...
│   └── ...
└── audio/                # Generated audio files
    └── ...
```

## License

MIT
