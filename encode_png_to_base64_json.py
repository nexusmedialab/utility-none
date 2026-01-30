#!/usr/bin/env python3
import argparse
import base64
import json
from pathlib import Path

def encode_png_to_data_uri(png_path):
    """Convert PNG file to base64 data URI string."""
    with open(png_path, 'rb') as f:
        png_data = f.read()
    b64_data = base64.b64encode(png_data).decode('utf-8')
    return f"data:image/png;base64,{b64_data}"

def process_directory(directory):
    """Process directory structure and return nested dict or list based on structure."""
    dir_path = Path(directory)
    
    # Check if directory has subdirectories with PNG files
    subdirs = [d for d in dir_path.iterdir() if d.is_dir()]
    png_files_in_root = list(dir_path.glob('*.png'))
    
    # Case 1: Flat structure (PNG files directly in root)
    if png_files_in_root and not any(list(d.rglob('*.png')) for d in subdirs):
        return sorted([{
            'name': f.name,
            'data': encode_png_to_data_uri(f)
        } for f in png_files_in_root], key=lambda x: x['name'])
    
    # Case 2: Nested structure (subdirectories contain PNG files)
    result = {}
    for subdir in sorted(subdirs):
        png_files = list(subdir.rglob('*.png'))
        if png_files:
            result[subdir.name] = sorted([{
                'name': f.name,
                'data': encode_png_to_data_uri(f)
            } for f in png_files], key=lambda x: x['name'])
    
    # Include root PNG files if they exist alongside subdirectories
    if png_files_in_root:
        result['_root'] = sorted([{
            'name': f.name,
            'data': encode_png_to_data_uri(f)
        } for f in png_files_in_root], key=lambda x: x['name'])
    
    return result if result else []

def main():
    parser = argparse.ArgumentParser(description='Convert PNG files to base64 data URIs')
    parser.add_argument('-d', '--directory', required=True, help='Input directory path')
    parser.add_argument('-o', '--output', required=True, help='Output JSON file path')
    
    args = parser.parse_args()
    
    dir_path = Path(args.directory)
    if not dir_path.exists():
        print(f"Error: Directory '{args.directory}' does not exist")
        return
    
    if not dir_path.is_dir():
        print(f"Error: '{args.directory}' is not a directory")
        return
    
    # Process directory
    png_data = process_directory(args.directory)
    
    # Create output structure
    output = {
        dir_path.name: png_data
    }
    
    # Write to JSON file
    with open(args.output, 'w') as f:
        json.dump(output, f, indent=2)
    
    file_count = len(png_data) if isinstance(png_data, list) else sum(len(v) for v in png_data.values())
    print(f"Processed {file_count} PNG files to {args.output}")

if __name__ == '__main__':
    main()
  
