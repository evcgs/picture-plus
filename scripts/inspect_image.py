#!/usr/bin/env python3
"""
Inspect image specifications: format, resolution, file size, aspect ratio.
Uses only built-in libraries - no PIL dependency for basic inspection.
"""

import os
import argparse
import struct

def png_get_dimensions(file_path):
    """Get PNG width and height without full PIL"""
    with open(file_path, 'rb') as f:
        # PNG signature check
        signature = f.read(8)
        if signature != b'\x89PNG\r\n\x1a\n':
            return None, None
        
        # Find IHDR chunk
        while True:
            chunk_length_data = f.read(4)
            if len(chunk_length_data) != 4:
                return None, None
            chunk_length = struct.unpack('>I', chunk_length_data)[0]
            
            chunk_type = f.read(4)
            if chunk_type == b'IHDR':
                # IHDR has width and height as 4-byte big-endian
                data = f.read(8)
                width = struct.unpack('>I', data[0:4])[0]
                height = struct.unpack('>I', data[4:8])[0]
                return width, height
            else:
                # Skip this chunk
                f.seek(chunk_length + 4, 1)  # chunk data + CRC

def jpeg_get_dimensions(file_path):
    """Get JPEG width and height without full PIL"""
    with open(file_path, 'rb') as f:
        f.seek(0)
        if f.read(2) != b'\xff\xd8':  # SOI marker
            return None, None
        
        while True:
            marker = f.read(1)
            if not marker:
                break
            if marker[0] != 0xff:
                continue
            
            marker_type = marker[0] << 8 | f.read(1)[0]
            
            if 0xffc0 <= marker_type <= 0xffc3:
                # Start of frame, has dimensions
                f.read(3)  # skip length and precision
                height = struct.unpack('>H', f.read(2))[0]
                width = struct.unpack('>H', f.read(2))[0]
                return width, height
            else:
                # Skip other segments
                length = struct.unpack('>H', f.read(2))[0]
                f.seek(length - 2, 1)
    
    return None, None

def inspect_image(image_path):
    """Inspect and print image specifications"""
    if not os.path.exists(image_path):
        print(f"Error: File not found - {image_path}")
        return None
    
    # Get file size
    file_size_bytes = os.path.getsize(image_path)
    file_size_kb = file_size_bytes / 1024
    file_size_mb = file_size_kb / 1024
    
    # Detect format and get dimensions
    ext = os.path.splitext(image_path)[1].lower()
    width = None
    height = None
    format_name = ext[1:].upper() if ext else "Unknown"
    
    if ext in ['.png']:
        width, height = png_get_dimensions(image_path)
        format_name = "PNG"
    elif ext in ['.jpg', '.jpeg']:
        width, height = jpeg_get_dimensions(image_path)
        format_name = "JPEG"
    
    print("=" * 50)
    print(f"Image Inspection: {os.path.basename(image_path)}")
    print("=" * 50)
    print(f"File path:     {image_path}")
    print(f"Format:        {format_name}")
    print(f"File size:     {file_size_kb:.1f} KB ({file_size_mb:.2f} MB)")
    
    if width and height:
        # Calculate aspect ratio
        aspect_ratio = width / height
        
        print(f"Resolution:    {width} × {height} = {width * height:,} pixels")
        print(f"Aspect ratio:  {aspect_ratio:.3f}")
        
        # Common aspect ratio suggestions
        common_ratios = {
            (1, 1): "1:1 (Square)",
            (16, 9): "16:9 (Widescreen)",
            (9, 16): "9:16 (Vertical)",
            (4, 3): "4:3 (Traditional)",
            (3, 4): "3:4 (Portrait)",
            (3, 2): "3:2 (Camera)",
        }
        
        print("\nCommon ratio match:")
        found_match = False
        for (w, h), name in common_ratios.items():
            ratio = w / h
            if abs(aspect_ratio - ratio) < 0.05:
                print(f"  → {name} (close match)")
                found_match = True
        if not found_match:
            print(f"  → Custom ratio")
        
        print("\nRecommended generation size matching this image:")
        print(f"  --width {width} --height {height}")
    else:
        print("\n⚠ Could not extract dimensions (unsupported format)")
        print("You'll need to specify --width and --height manually")
    
    print("=" * 50)
    
    return {
        "path": image_path,
        "filename": os.path.basename(image_path),
        "format": format_name,
        "width": width,
        "height": height,
        "total_pixels": width * height if width and height else None,
        "file_size_bytes": file_size_bytes,
        "aspect_ratio": width / height if width and height else None,
    }

def main():
    parser = argparse.ArgumentParser(description='Inspect image specifications')
    parser.add_argument('--image', required=True, help='Path to image file')
    args = parser.parse_args()
    
    inspect_image(args.image)

if __name__ == '__main__':
    main()
