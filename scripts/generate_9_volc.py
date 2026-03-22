#!/usr/bin/env python3
"""
Generate 9 images with consistent style from reference using Volcengine Seedream.
Usage:
python generate_9_volc.py --reference /path/to/ref.png --prompt "your prompt" --output ./output
"""

import os
import argparse
import json
import base64
import urllib.request
import urllib.error
from PIL import Image
from typing import List, Dict

VOLCENGINE_API_KEY = os.environ.get('VOLCENGINE_API_KEY') or os.environ.get('ARK_API_KEY')
if not VOLCENGINE_API_KEY:
    raise ValueError("VOLCENGINE_API_KEY or ARK_API_KEY environment variable not set")

API_ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
MODEL = "doubao-seedream-4-5-251128"

def encode_image(image_path: str) -> str:
    """Encode image to base64"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def generate_image(reference_b64: str, prompt: str, width: int, height: int) -> bytes:
    """Generate a single image using Volcengine API with reference style"""
    
    # Build the full prompt with reference
    full_prompt = f"{prompt}。请参考上传的参考图片，严格匹配参考图片的风格、配色、设计风格，保持相同的简约扁平设计风格。"
    
    headers = {
        "Authorization": f"Bearer {VOLCENGINE_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL,
        "prompt": full_prompt,
        "width": width,
        "height": height,
        "response_format": "b64_json",
        "image_ref": [
            {
                "image": reference_b64,
                "ref_type": "style"
            }
        ]
    }
    
    req = urllib.request.Request(
        API_ENDPOINT,
        data=json.dumps(data).encode('utf-8'),
        headers=headers
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            if "data" in result and len(result["data"]) > 0:
                image_b64 = result["data"][0]["b64_json"]
                return base64.b64decode(image_b64)
            else:
                print(f"  × No image data in response: {result}")
                return None
    except urllib.error.URLError as e:
        print(f"  × Request error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"  × JSON decode error: {e}")
        return None

def create_3x3_collage(image_paths: List[str], output_path: str) -> None:
    """Create a 3x3 collage from 9 image paths"""
    if len(image_paths) != 9:
        print(f"Warning: Expected 9 images for collage, got {len(image_paths)}")
        return
    
    try:
        # Open all images and get their sizes
        images = [Image.open(img) for img in image_paths]
        single_w, single_h = images[0].size
        
        # Create collage
        collage = Image.new('RGB', (single_w * 3, single_h * 3))
        
        for idx, img in enumerate(images):
            row = idx // 3
            col = idx % 3
            collage.paste(img, (col * single_w, row * single_h))
        
        collage.save(output_path, quality=95)
        print(f"✓ Collage saved to: {output_path}")
        
        # Cleanup
        for img in images:
            img.close()
    except Exception as e:
        print(f"⚠ Failed to create collage: {e}")
        return

def main():
    parser = argparse.ArgumentParser(description='Generate 9 images with consistent style from reference (Volcengine Doubao)')
    parser.add_argument('--reference', required=True, help='Path to reference image (for style matching)')
    parser.add_argument('--prompt', required=True, help='Text prompt describing what content to generate')
    parser.add_argument('--output', required=True, help='Output directory for generated images')
    parser.add_argument('--width', type=int, help='Target width (defaults to reference width)', default=None)
    parser.add_argument('--height', type=int, help='Target height (defaults to reference height)', default=None)
    
    args = parser.parse_args()
    
    # Get reference dimensions if not provided
    if args.width is None or args.height is None:
        with Image.open(args.reference) as img:
            ref_w, ref_h = img.size
            args.width = args.width or ref_w
            args.height = args.height or ref_h
    
    print(f"Target size: {args.width} × {args.height}")
    print(f"Model: {MODEL}")
    print(f"Generating 9 images...")
    print(f"Prompt: {args.prompt}")
    print(f"Reference: {args.reference}")
    print(f"Output dir: {args.output}")
    
    # Create output directory
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # Encode reference image once
    reference_b64 = encode_image(args.reference)
    
    results = []
    
    # Generate 9 images one by one
    for i in range(9):
        print(f"\nGenerating image {i+1}/{9}...")
        
        image_data = generate_image(reference_b64, args.prompt, args.width, args.height)
        
        if image_data:
            output_filename = f"{i+1:02d}.png"
            output_path = os.path.join(args.output, output_filename)
            
            with open(output_path, 'wb') as f:
                f.write(image_data)
            
            # Verify
            w, h = None, None
            try:
                with Image.open(output_path) as img:
                    w, h = img.size
                    print(f"  ✓ Saved to {output_path} ({w}×{h})")
            except Exception as e:
                print(f"  ⚠ Image saved but verification failed: {e}")
            
            results.append({
                "index": i+1,
                "path": output_path,
                "filename": output_filename,
                "success": True,
                "width": w,
                "height": h
            })
        else:
            results.append({
                "index": i+1,
                "success": False,
                "error": "Generation failed"
            })
    
    # Save metadata
    metadata = {
        "reference": args.reference,
        "prompt": args.prompt,
        "count": 9,
        "width": args.width,
        "height": args.height,
        "output_dir": args.output,
        "provider": "volcengine",
        "model": MODEL,
        "results": results
    }
    
    metadata_path = os.path.join(args.output, "metadata.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Metadata saved to: {metadata_path}")
    
    # Create collage from successful results
    successful_paths = [r["path"] for r in results if r["success"]]
    if len(successful_paths) >= 9:
        collage_path = os.path.join(args.output, "collage-3x3.png")
        create_3x3_collage(successful_paths[:9], collage_path)
    
    # Summary
    success_count = sum(1 for r in results if r["success"])
    print(f"\n{'='*50}")
    print(f"Generation complete: {success_count}/{len(results)} images succeeded")
    print(f"{'='*50}")
    
    if success_count == 0:
        print("\n⚠ All generations failed. Check your API key and quota.")
        exit(1)

if __name__ == '__main__':
    # Fix for environment variable name
    if 'VOLCENGINE_API_KEY' in os.environ:
        VOLCENGINE_KEY = os.environ['VOLCENGINE_API_KEY']
    else:
        VOLCENGINE_KEY = os.environ['ARK_API_KEY']
    main()
