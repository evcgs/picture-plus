---
name: picture-plus
description: Image generation with style reference matching. Supports Google Gemini and Volcengine Doubao Seedream. Inspect image specs, batch generate 9 images with consistent style.
homepage: https://github.com/yourusername/picture-plus
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["python3"], "env": ["GOOGLE_API_KEY", "VOLCENGINE_API_KEY"] },
        "install":
          [
            {
              "id": "python-brew",
              "kind": "brew",
              "formula": "python",
              "bins": ["python3"],
              "label": "Install Python (brew)",
            },
          ],
      },
  }
---

# Picture Plus 🎨

Image generation with **reference style matching**. Generate 9 images with consistent style from a single reference image. Supports both Google Gemini and Volcengine Doubao Seedream.

## Features

- ✅ **Inspect image specs** - Check resolution, file size, aspect ratio before generation
- ✅ **Reference style matching** - Upload one reference image, generate new images that match its style
- ✅ **Batch generate 9 images** - One click to get 9 consistently-styled images (perfect for 3x3 grids)
- ✅ **Dual provider support** - Use either Google Gemini or Volcengine Doubao Seedream
- ✅ **Auto collage** - Creates a 3x3 preview collage for easy selection
- ✅ **Flexible sizing** - Auto-match reference size or specify custom dimensions
- ✅ **Works in chat** - Send reference image directly in chat, get generated images back

---

## Prerequisites

### Install dependencies
```bash
pip3 install google-generativeai pillow requests
```

### API Keys

You need at least one API key:

| Provider | Get API Key | Environment Variable |
|----------|--------------|-----------------------|
| Google Gemini | https://makersuite.google.com/app/apikey | `GOOGLE_API_KEY` |
| Volcengine Doubao | https://console.volcengine.com/ark | `VOLCENGINE_API_KEY` (or `ARK_API_KEY`) |

Add your API keys to `~/.openclaw/.env`:
```bash
echo "GOOGLE_API_KEY=your_key_here" >> ~/.openclaw/.env
echo "VOLCENGINE_API_KEY=your_key_here" >> ~/.openclaw/.env
```

---

## Usage

### 1. Inspect an image (check specs before generation)
```bash
python3 {baseDir}/scripts/inspect_image.py --image /path/to/reference.png
```

This will show you:
- File format, size, resolution
- Aspect ratio detection
- Recommended generation size matching the reference

### 2. Generate 9 images with Google Gemini
```bash
python3 {baseDir}/scripts/generate_9_gemini.py \
  --reference /path/to/reference.png \
  --prompt "Your description here" \
  --output ./output-folder
```

Specify custom size:
```bash
python3 {baseDir}/scripts/generate_9_gemini.py \
  --reference /path/to/reference.png \
  --prompt "Your description here" \
  --width 1024 --height 1024 \
  --output ./output-folder
```

### 3. Generate 9 images with Volcengine Doubao (recommended for China)
```bash
python3 {baseDir}/scripts/generate_9_volc.py \
  --reference /path/to/reference.png \
  --prompt "Your description here" \
  --output ./output-folder
```

Specify custom size:
```bash
python3 {baseDir}/scripts/generate_9_volc.py \
  --reference /path/to/reference.png \
  --prompt "Your description here" \
  --width 1080 --height 1440 \
  --output ./output-folder
```

### 4. Generate fewer images (1-4)
```bash
python3 {baseDir}/scripts/generate_gemini.py \
  --reference /path/to/reference.png \
  --prompt "Your description here" \
  --count 4 \
  --output ./output-folder
```

---

## Usage in OpenClaw Chat

You don't need to use the command line! Just:

1. **Send your reference image** directly in the chat window
2. **Tell me your prompt** - what content do you want to generate?
3. **Tell me your desired size** (optional, defaults to reference size)
4. **I'll run it for you** and send back all 9 generated images!

Example chat conversation:
```
You: [sends reference image]
You: Generate 9 images of common food, matching this style, size 1024x1024
Me: ✓ Generating... (after a few minutes) sends back all 9 images + collage
```

---

## Output Structure

After generation, your output folder will contain:
```
output-folder/
├── 01.png
├── 02.png
├── 03.png
├── 04.png
├── 05.png
├── 06.png
├── 07.png
├── 08.png
├── 09.png
├── collage-3x3.png    (3x3 grid preview for easy selection)
└── metadata.json      (all generation info for reference)
```

---

## Prompt Tips for Style Matching

When using style reference, your prompt should include:

1. **Content description** - What do you want in the new images?
2. **Explicit style matching** - "Match the exact style of the reference image"
3. **Composition** - "Centered composition, clean background, etc."

Example good prompt:
```
A collection of common breakfast foods, each image shows one item. Match the same minimalist flat design style as the reference image, clean simple colors, centered composition.
```

---

## Size Recommendations

| Use Case | Size | Aspect Ratio |
|----------|------|--------------|
| Square icons | 1024x1024 | 1:1 |
| WeChat inline | 1080x1440 | 3:4 |
| WeChat cover | 1280x720 | 16:9 |
| Mobile wallpaper | 1080x2340 | 9:16 |

---

## Notes

- Google Gemini free tier has rate limits. If you get quota errors, wait a day or switch to paid.
- Volcengine Doubao works great in China, no VPN needed.
- Style matching isn't pixel-perfect - some variation is normal, that's why we generate 9 options!
- All images are saved locally, you can pick the best one.

---

## Examples

Check the `examples/` folder for example workflows.

## License

MIT
