# Picture Plus 🎨 - Image Generation with Style Reference

[中文 README 点击这里](./README.zh-CN.md)

Generate **9 images with consistent style** from a single reference image.  
Supports both **Google Gemini** and **Volcengine Doubao Seedream**.

## Features

- ✅ Inspect image specifications (resolution, size, aspect ratio)
- ✅ Style matching from reference image
- ✅ Batch generate exactly 9 images (perfect for 3x3 grids)
- ✅ Auto-create 3x3 preview collage
- ✅ Two providers to choose from: Google Gemini / Volcengine Doubao
- ✅ Flexible sizing: auto-match reference or custom size
- ✅ Works both in command line and OpenClaw chat

## Installation

### 1. Install the skill
```bash
# If installing via OpenClaw skills
npx skills add yourusername/picture-plus
```

### 2. Install Python dependencies
```bash
pip3 install google-generativeai pillow
```

### 3. Configure API Keys

You need **at least one** API key:

| Provider | Where to get | Environment Variable |
|----------|--------------|-----------------------|
| Google Gemini | [Google AI Studio](https://makersuite.google.com/app/apikey) | `GOOGLE_API_KEY` |
| Volcengine Doubao | [Volcengine Ark](https://console.volcengine.com/ark) | `VOLCENGINE_API_KEY` |

Add them to your `~/.openclaw/.env` file:
```bash
# Add these lines at the end
GOOGLE_API_KEY=your_google_api_key_here
VOLCENGINE_API_KEY=your_volcengine_api_key_here
```

## Quick Start

### Method 1: Use in OpenClaw Chat (Recommended)

It's super simple:

1. **Send your reference image** to the chat
2. **Tell me what you want**:  
   `Generate 9 images of [your content], matching this style, size 1024x1024`
3. **Wait a few minutes** - I'll run it and send you all 9 images + preview collage!

Example:
```
You: [upload your reference image]
You: Generate 9 images of common daily objects, match this minimalist flat style, 1024x1024
Me: ✓ Done! Sends you all 9 images + 3x3 collage
```

### Method 2: Command Line Usage

#### Step 1: Inspect your reference image
```bash
python3 scripts/inspect_image.py --image /path/to/reference.png
```

This tells you:
- Current resolution
- Aspect ratio
- Recommended size matching

#### Step 2: Generate 9 images

**With Google Gemini:**
```bash
python3 scripts/generate_9_gemini.py \
  --reference /path/to/reference.png \
  --prompt "Your description here, match the style of the reference image" \
  --output ./output-directory
```

**With Volcengine Doubao (better for China access):**
```bash
python3 scripts/generate_9_volc.py \
  --reference /path/to/reference.png \
  --prompt "Your description here, match the style of the reference image" \
  --output ./output-directory
```

**Specify custom size:**
```bash
# Add --width and --height
python3 scripts/generate_9_volc.py \
  --reference /path/to/reference.png \
  --prompt "Your content" \
  --width 1080 --height 1440 \
  --output ./output
```

## Output Files

After generation, you get:

```
output-directory/
├── 01.png - 09.png    # 9 individual images
├── collage-3x3.png     # Preview all 9 in a 3x3 grid
└── metadata.json      # Generation info for reference
```

## Recommended Sizes

| Use Case | Size | Aspect Ratio |
|----------|------|--------------|
| Square icons/avatars | 1024×1024 | 1:1 |
| WeChat public account inline | 1080×1440 | 3:4 |
| WeChat cover image | 1280×720 | 16:9 |
| Mobile wallpaper | 1080×2340 | 9:16 |

If you don't specify size, it **automatically uses the reference image size**.

## Writing Good Prompts for Style Matching

To get the best style matching, include these in your prompt:

1. **Describe what you want** (content)
2. **Explicitly say "match the style of the reference image"**
3. **Add composition details** (centered, clean background, etc.)

✅ **Good example:**
```
9 different types of coffee cups, each image shows one coffee cup. Match the exact minimalist flat design style from the reference image, clean solid colors, centered composition, white background.
```

❌ **Bad example (too vague):**
```
coffee cups same style
```

## Tips

- **Style matching isn't pixel-perfect** - that's why we generate 9 options, pick the one you like best!
- **Google Gemini free tier** has daily quota limits. If you get errors, wait a day or use Volcengine.
- **Volcengine** works great from China, no VPN needed.
- **All images are saved locally** - you keep full control.

## Example Workflow

Here's what a full run looks like in chat:

1. You send reference image → "Generate 9 daily objects matching this style, 1024x1024"
2. I inspect the image → confirm size
3. I run the generation → 9 images done
4. I send you the 3x3 collage preview → then send all individual images
5. You pick the ones you want to use!

## Issues & Troubleshooting

**Q: I get "quota exceeded" from Google**  
A: Free tier is limited. Either wait 24h, upgrade to paid, or use Volcengine instead.

**Q: The style doesn't match very well**  
A: Try adding "strictly match the style, colors, and design of the reference image" to your prompt. Generating 9 gives you variation - pick the closest match.

**Q: Can I generate fewer than 9 images?**  
A: Yes, use `generate_gemini.py` or `generate_volc.py` with `--count N` where N is 1-4.

## License

MIT
