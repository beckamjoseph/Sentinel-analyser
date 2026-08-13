#!/usr/bin/env python3
"""
Create placeholder PNG icons for Chrome extension.
"""

try:
    from PIL import Image, ImageDraw
    import os

    def create_icon(size, output_path):
        """Create a simple gradient icon."""
        # Create image with gradient
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Create gradient from purple to blue
        for y in range(size):
            r = int(102 + (118 - 102) * y / size)
            g = int(126 + (75 - 126) * y / size)
            b = int(234 + (162 - 234) * y / size)
            draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
        
        # Draw shield shape
        margin = size // 8
        shield_points = [
            (size // 2, margin),
            (size - margin, margin + size // 4),
            (size - margin, size // 2 + size // 4),
            (size // 2, size - margin),
            (margin, size // 2 + size // 4),
            (margin, margin + size // 4)
        ]
        draw.polygon(shield_points, fill=(255, 255, 255, 200), outline=(255, 255, 255, 255), width=2)
        
        # Draw checkmark
        if size >= 32:
            checkmark_points = [
                (size // 3, size // 2),
                (size // 2, size // 2 + size // 6),
                (size // 2 + size // 3, size // 3)
            ]
            draw.line(checkmark_points, fill=(255, 255, 255, 255), width=max(2, size // 16))
        
        img.save(output_path, 'PNG')
        print(f"Created {output_path} ({size}x{size})")

    def create_all_icons():
        """Create all required icon sizes."""
        output_dir = 'icons'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        sizes = [16, 48, 128]
        for size in sizes:
            output_path = os.path.join(output_dir, f'icon{size}.png')
            create_icon(size, output_path)
        
        print("All placeholder icons created successfully!")

    if __name__ == '__main__':
        create_all_icons()

except ImportError:
    print("PIL not installed. Install with: pip install pillow")
    print("Or use online tools to convert icons/icon.svg to PNG files.")