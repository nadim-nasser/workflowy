#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# LinkedIn cover dimensions
WIDTH = 1584
HEIGHT = 396

# Create image with dark gradient background
img = Image.new('RGB', (WIDTH, HEIGHT), '#0f172a')
draw = ImageDraw.Draw(img)

# Create gradient background effect
for x in range(WIDTH):
    for y in range(HEIGHT):
        # Create a subtle diagonal gradient
        factor = (x / WIDTH + y / HEIGHT) / 2
        r = int(15 + factor * 15)
        g = int(23 + factor * 18)
        b = int(42 + factor * 17)
        draw.point((x, y), fill=(r, g, b))

# Add subtle grid pattern
grid_color = (255, 255, 255, 8)
for x in range(0, WIDTH, 60):
    draw.line([(x, 0), (x, HEIGHT)], fill=(30, 41, 59), width=1)
for y in range(0, HEIGHT, 60):
    draw.line([(0, y), (WIDTH, y)], fill=(30, 41, 59), width=1)

# Add glowing circles (decorative)
def draw_glow_circle(draw, cx, cy, r, color, alpha):
    for i in range(r, 0, -2):
        a = int(alpha * (i / r))
        c = (*color, a)
        # Since we can't use alpha directly, we'll simulate with color blending
        pass

# Add decorative elements (subtle colored areas)
draw.ellipse([(-50, -100), (250, 200)], fill=(20, 30, 50), outline=None)
draw.ellipse([(1350, 250), (1650, 500)], fill=(25, 28, 52), outline=None)

# Try to load a system font, fall back to default
try:
    font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
    font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
except:
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/SFNSDisplay.ttf", 48)
        font_medium = ImageFont.truetype("/System/Library/Fonts/SFNSDisplay.ttf", 20)
        font_small = ImageFont.truetype("/System/Library/Fonts/SFNSDisplay.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

# Main text - positioned to avoid logo area (left ~200px is logo zone)
# "Bridge the Enterprise"
draw.text((450, 100), "Bridge the Enterprise", fill='#ffffff', font=font_large)

# "AI Skills Gap" with gradient effect (approximate with blue-purple)
draw.text((450, 160), "AI Skills Gap", fill='#818cf8', font=font_large)

# Subheadline
draw.text((450, 235), "From pilots to production. Training that delivers ROI.", fill='#94a3b8', font=font_medium)

# Accent line (gradient bar)
for x in range(450, 650):
    progress = (x - 450) / 200
    r = int(59 + progress * (139 - 59))
    g = int(130 + progress * (92 - 130))
    b = int(246 + progress * (246 - 246))
    draw.line([(x, 280), (x, 284)], fill=(r, g, b), width=1)

# Feature pills on right side
pills = [
    ("Live Builds", (59, 130, 246), 90),
    ("Your Tools", (139, 92, 246), 145),
    ("Measurable ROI", (16, 185, 129), 200)
]

for text, color, y_offset in pills:
    # Pill background
    pill_x = 1100
    pill_y = y_offset
    pill_width = 160
    pill_height = 32

    # Draw rounded rectangle (pill shape)
    bg_color = (color[0]//4, color[1]//4, color[2]//4)
    draw.rounded_rectangle(
        [(pill_x, pill_y), (pill_x + pill_width, pill_y + pill_height)],
        radius=16,
        fill=bg_color
    )

    # Pill text
    text_color = (color[0] + 60, min(color[1] + 60, 255), min(color[2] + 60, 255))
    bbox = draw.textbbox((0, 0), text, font=font_small)
    text_width = bbox[2] - bbox[0]
    text_x = pill_x + (pill_width - text_width) // 2
    text_y = pill_y + 7
    draw.text((text_x, text_y), text, fill=text_color, font=font_small)

# Website URL
draw.text((1420, 355), "workflowy.ai", fill='#64748b', font=font_small)

# Save
output_path = '/Users/nadimnasser/GitHub/workflowy/linkedin-cover-1584x396.png'
img.save(output_path, 'PNG', quality=95)
print(f"Created: {output_path}")
print(f"Size: {img.size}")
