#!/usr/bin/env python3
"""
Generate PNG icons from SVG for Chrome extension.
Requires: pip install cairosvg pillow
"""

try:
    import cairosvg
    from PIL import Image
    import io
    import os

    def svg_to_png(svg_path, png_path, size):
        """Convert SVG to PNG at specified size."""
        # Convert SVG to PNG bytes
        png_data = cairosvg.svg2png(url=svg_path, output_width=size, output_height=size)
        
        # Load into PIL and save
        img = Image.open(io.BytesIO(png_data))
        img.save(png_path, 'PNG')
        print(f"Generated {png_path} ({size}x{size})")

    def generate_icons():
        """Generate all required icon sizes."""
        svg_path = 'icons/icon.svg'
        output_dir = 'icons'
        
        if not os.path.exists(svg_path):
            print(f"Error: {svg_path} not found")
            return
        
        sizes = [16, 48, 128]
        
        for size in sizes:
            png_path = os.path.join(output_dir, f'icon{size}.png')
            svg_to_png(svg_path, png_path, size)
        
        print("All icons generated successfully!")

    if __name__ == '__main__':
        generate_icons()

except ImportError:
    print("Required packages not installed.")
    print("Install them with: pip install cairosvg pillow")
    print("\nAlternatively, you can use online tools to convert the SVG to PNG:")
    print("1. Open icons/icon.svg in a browser")
    print("2. Use a screenshot tool or online converter")
    print("3. Save as icon16.png, icon48.png, and icon128.png")