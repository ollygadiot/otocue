# Notation Guide for LLMs

When converting plain script text to Otocue teleprompter notation, apply these rules to add meaning, pacing, and delivery cues.

## Pause Notation

| Notation | Description |
|----------|-------------|
| `•` | Short breath pause. Use between clauses, list items, or before important words. Creates rhythm. |
| `• • •` | Long dramatic pause. Use before reveals, after questions, or when letting an idea land. 2-3 seconds. |
| `//` | Complete silence/beat. Use alone on its own line for dramatic effect. Eye contact moment, no words. |

## Emphasis Notation

| Notation | Description |
|----------|-------------|
| `**word**` | Strong emphasis with glow. Use for: key concepts the viewer must remember, contrasts ("not this, **this**"), emotional peaks, numbers and specifics that matter. |
| `_word_` | Soft/understated. Use for: parenthetical asides, self-deprecating moments, words that trail off, humble or reflective phrases. |

## Speed Notation

| Notation | Description |
|----------|-------------|
| `<<text>>` | Slow down. Use for: important realizations, emotional weight, final lines that need to land, complex ideas needing absorption. |
| `>>text<<` | Speed up. Use for: lists and montage sections, building energy/excitement, less important connective phrases, rapid-fire examples. |

## Pitch Notation

| Notation | Description |
|----------|-------------|
| `^word^` | Pitch rises. Use for: questions (rhetorical or real), curiosity and wonder, inviting the viewer in, setting up anticipation. |
| `,word,` | Pitch drops. Use for: conclusions and finality, gravity and weight, statements of fact, endings of thoughts. |

## Volume Notation

| Notation | Description |
|----------|-------------|
| `WORD` | Loud/punchy (all caps). Use for: single-word impact moments, commands or calls to action, breakthrough moments. Maximum 1-2 words at a time. |
| `~word~` | Whisper/intimate. Use for: vulnerability, secrets or confessions, drawing the viewer closer, painful admissions. |

## Style/Emotion Notation

For TTS generation with Azure DavisNeural voice:

| Notation | Description |
|----------|-------------|
| `{style:text}` | Apply emotional style to text |
| `{style,degree:text}` | Style with intensity (0.5=subtle, 2=intense) |

### Available Styles

| Style | Use For |
|-------|---------|
| `cheerful` | Happy, upbeat moments |
| `excited` | High energy, breakthroughs |
| `sad` | Loss, disappointment, reflection |
| `hopeful` | Optimism, looking forward |
| `empathetic` | Understanding, connection |
| `friendly` | Warm, approachable |
| `calm` | Soothing, relaxed |
| `angry` | Frustration (use sparingly) |
| `terrified` | Fear, anxiety |
| `shouting` | Loud exclamation |
| `whispering` | Intimate, secret |

### Examples

```
{excited: This is amazing!}
{sad,0.5: I was stuck for years}
{hopeful: Could this be the key?}
```

---

## Conversion Examples

### Example 1

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

### Example 2

**Plain text:**
```
Could this closet be the key to finally building all my projects?
```

**With notation:**
```
^Could this closet be the key^ •to finally building all the projects I've been dreaming about for _years_?
```

**Why:**
- Rising pitch for the question (`^...^`)
- Breath before the emotional part (`•`)
- Soft on "years" to show vulnerability (`_..._`)

### Example 3

**Plain text:**
```
Gone.
```

**With notation:**
```
,**Gone**,.
```

**Why:**
- Pitch down for finality (`,...,`)
- Strong emphasis for impact (`**`)
- Single word = maximum power

---

## Conversion Principles

### 1. Less Is More
Don't mark every word. Reserve notation for moments that matter. A script with too much notation becomes noise.

### 2. Contrast Creates Meaning
Slow sections need fast sections. Whispers need loud moments. The power comes from the difference.

### 3. Pauses Are Punctuation
- Use `•` like commas for rhythm
- Use `• • •` like periods for letting ideas land
- Use `//` like paragraph breaks for major transitions

### 4. Match Content to Form
| Content | Notation |
|---------|----------|
| Questions | `^pitch up^` |
| Answers | `,pitch down,` |
| Lists | `>>speed up<<` |
| Insights | `<<slow down>>` |
| Pain | `~whisper~` |
| Triumph | `**LOUD**` |

### 5. Serve the Story
Every notation should help the speaker deliver the emotional truth. If a mark doesn't serve the story, remove it.

---

## Gesture Notation

Add body language cues using the `gesture` property on segments. Gestures display as icons in the teleprompter to remind the speaker of effective body language.

### JSON Format

```json
{
  "line": "Welcome to my presentation.",
  "format": "on-camera",
  "gesture": "arms-open"
}
```

### Available Gestures

| Gesture ID        | Description                           | When to Use                                      |
|-------------------|---------------------------------------|--------------------------------------------------|
| `palm-up`         | Open palm facing up                   | Welcoming, questions, showing transparency       |
| `palm-down`       | Palm facing down                      | Calming, authoritative, settling a point         |
| `open-hands`      | Both palms visible                    | Openings, conclusions, honest admissions         |
| `measure-loaf`    | Hands apart, palms facing             | Framing content, showing scope                   |
| `pinching`        | Thumb and finger pinched              | Key details, precise points                      |
| `point-at-viewer` | Index finger forward                  | Direct address, "this applies to YOU"            |
| `index-up`        | Fist with thumb up                    | Emphasis without accusation                      |
| `thumbs-up`       | Approval gesture                      | Positive reinforcement, "that's right"           |
| `countdown-1`     | One finger raised                     | "First..." or single important point             |
| `countdown-2`     | Two fingers                           | "Second..." or two options                       |
| `countdown-3`     | Three fingers                         | "Third..." or three points                       |
| `countdown-4`     | Four fingers                          | "Fourth..."                                      |
| `countdown-5`     | Full hand                             | "Fifth..." or high-five moment                   |
| `compare`         | Two hands in different positions      | "On one hand... on the other..."                 |
| `heart-touch`     | Hand over heart                       | Personal stories, sincere moments                |
| `folded-hands`    | Hands together                        | Gratitude, requests, "please"                    |
| `expand-clasp`    | Hands coming together                 | Bringing ideas together, synthesis               |
| `raising-hands`   | Both hands raised                     | Celebration, victory, excitement                 |
| `arms-open`       | Arms spread wide                      | Big moments, welcoming, grand statements         |
| `arms-sides`      | Neutral resting position              | Pauses, listening, reset                         |
| `flexed-biceps`   | Flexed arm                            | Strength, determination, power                   |

### Gesture Guidelines for LLMs

1. **Use sparingly** - Not every segment needs a gesture. Add them for key moments.
2. **Match content** - Gestures should reinforce the message:
   - Welcoming statements → `arms-open` or `palm-up`
   - Questions → `palm-up` or `point-up`
   - Lists → `countdown-1`, `countdown-2`, etc.
   - Comparisons → `compare`
   - Personal moments → `heart-touch`
   - Conclusions → `expand-clasp` or `palm-down`
3. **Avoid overuse** - A gesture every 3-5 segments is usually enough.
4. **Consider the flow** - Vary gestures; don't repeat the same one consecutively.

### Example with Gestures

```json
{
  "chapters": [
    {
      "chapter": "Introduction",
      "segments": [
        {
          "line": "Welcome everyone to today's talk.",
          "format": "on-camera",
          "gesture": "arms-open"
        },
        {
          "line": "I want to share **three insights** with you.",
          "format": "on-camera",
          "gesture": "countdown-3"
        },
        {
          "line": "First, •the power of simplicity.",
          "format": "on-camera",
          "gesture": "countdown-1"
        },
        {
          "line": "This truly changed how I work.",
          "format": "on-camera",
          "gesture": "heart-touch"
        }
      ]
    }
  ]
}
```
