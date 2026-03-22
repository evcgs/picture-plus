#!/usr/bin/env python3
"""
Generate 9 images with consistent style from a reference image using Google Gemini.
Usage:
python generate_9_gemini.py --reference reference.jpg --prompt "your prompt" --output ./output
"""

import os
import argparse
import json
import google.generativeai as genai
from PIL import Image
from typing import List, Dict

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=GOOGLE_API_KEY)

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

def generate_images(reference_path: str, prompt: str, count: int, width: int, height: int, output_dir: str) -> List[Dict]:
    """Generate N images with reference style matching"""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load reference image
    reference_img = Image.open(reference_path)
    
    # Create the model - use gemini-2.5-flash-image which is optimized for image generation
    # Gemini 2.5 Flash Image supports image input and generation natively
    model = genai.GenerativeModel('models/gemini-2.5-flash-image')
    
    # Build the full prompt
    full_prompt = f"""I will provide a reference image. I want you to generate {count} new images that match the STYLE of the reference image exactly, but with the following content:

{prompt}

Important instructions:
1. Match the visual style, color palette, level of detail, and composition style of the reference image
2. Each of the {count} images should be consistent in style with each other and with the reference
3. Output each image as a separate generation
4. The images should be {width} × {height} pixels

Generate the {count} images now:"""
    
    print(f"Generating {count} images...")
    print(f"Prompt: {prompt}")
    print(f"Reference: {reference_path}")
    print(f"Output dir: {output_dir}")
    
    results = []
    
    # Gemini doesn't do batch generation natively, so we generate one by one
    # Each generation gets the reference + the prompt to ensure style consistency
    for i in range(count):
        print(f"\nGenerating image {i+1}/{count}...")
        
        try:
            response = model.generate_content([full_prompt, reference_img])
            response.resolve()
            
            # Check if response has candidates
            if not response.candidates:
                print(f"  × Failed to generate image {i+1}: No candidates")
                results.append({
                    "index": i+1,
                    "success": False,
                    "error": "No candidates"
                })
                continue
            
            # Extract image from response
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    # Save the image
                    output_filename = f"{i+1:02d}.png"
                    output_path = os.path.join(output_dir, output_filename)
                    
                    with open(output_path, 'wb') as f:
                        f.write(part.inline_data.data)
                    
                    # Verify the image
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
                    break
            else:
                print(f"  × No image found in response for image {i+1}")
                results.append({
                    "index": i+1,
                    "success": False,
                    "error": "No image in response"
                })
                
        except Exception as e:
            print(f"  × Error generating image {i+1}: {str(e)}")
            results.append({
                "index": i+1,
                "success": False,
                "error": str(e)
            })
    
    reference_img.close()
    return results

def main():
    parser = argparse.ArgumentParser(description='Generate 9 images with consistent style from reference (Google Gemini)')
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
    
    # Generate 9 images
    results = generate_images(
        reference_path=args.reference,
        prompt=args.prompt,
        count=9,
        width=args.width,
        height=args.height,
        output_dir=args.output
    )
    
    # Save metadata
    metadata = {
        "reference": args.reference,
        "prompt": args.prompt,
        "count": 9,
        "width": args.width,
        "height": args.height,
        "output_dir": args.output,
        "provider": "google-gemini",
        "model": "gemini-2.5-flash-image",
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
    main()
