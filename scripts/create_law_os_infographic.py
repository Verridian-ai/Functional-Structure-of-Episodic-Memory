"""
Verridian LAW OS Features Infographic Generator
Creates a professional dark-themed infographic showcasing all major features
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# Dimensions (16:9 ratio, 4K quality)
WIDTH = 1920
HEIGHT = 1080

# Colors
CHARCOAL_BG = "#0f0f1a"
CARD_BG = "#1a1a2e"
CARD_BORDER = "#2d2d44"
EMERALD = "#10b981"
EMERALD_DARK = "#059669"
EMERALD_GLOW = "#34d399"
WHITE = "#ffffff"
GRAY_TEXT = "#9ca3af"
LIGHT_GRAY = "#e5e7eb"

# Feature data
FEATURES = [
    {"icon": "chat", "title": "Chat Interface", "desc": "AI-powered legal conversations with streaming"},
    {"icon": "voice", "title": "Voice Input", "desc": "Push-to-talk with real-time transcription"},
    {"icon": "graph", "title": "3D Knowledge Graph", "desc": "Interactive citation network (5,000+ nodes)"},
    {"icon": "doc", "title": "Document Generation", "desc": "PDF/DOCX export with templates"},
    {"icon": "canvas", "title": "Canvas Editor", "desc": "Rich document creation with formatting"},
    {"icon": "memory", "title": "Memory Integration", "desc": "Persistent episodic memory (Mem0)"},
    {"icon": "gsw", "title": "GSW Legal Analysis", "desc": "Temporal Episodic Memory + VSA"},
    {"icon": "image", "title": "Image Generation", "desc": "AI infographics with NanoBanana Pro"},
    {"icon": "admin", "title": "Admin Settings", "desc": "Model config, tools, MCP servers"},
    {"icon": "responsive", "title": "Responsive Design", "desc": "Desktop and mobile support"},
]

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def draw_rounded_rect(draw, coords, radius, fill, outline=None, width=1):
    """Draw a rounded rectangle"""
    x1, y1, x2, y2 = coords

    # Draw main rectangle
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)

    # Draw corners
    draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
    draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)

    if outline:
        # Draw outline
        draw.arc([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=outline, width=width)
        draw.arc([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1 + radius, y1, x2 - radius, y1], fill=outline, width=width)
        draw.line([x1 + radius, y2, x2 - radius, y2], fill=outline, width=width)
        draw.line([x1, y1 + radius, x1, y2 - radius], fill=outline, width=width)
        draw.line([x2, y1 + radius, x2, y2 - radius], fill=outline, width=width)

def draw_icon(draw, icon_type, x, y, size, color):
    """Draw feature icons using simple shapes"""
    r = hex_to_rgb(color)

    if icon_type == "chat":
        # Chat bubble icon
        draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//3], fill=r)
        draw.polygon([(x-size//4, y+size//4), (x-size//2, y+size//2), (x, y+size//4)], fill=r)
        # Smaller bubble
        draw.ellipse([x+size//4, y-size//4, x+size//2+5, y], fill=r)

    elif icon_type == "voice":
        # Microphone icon
        draw.ellipse([x-size//6, y-size//2, x+size//6, y], fill=r)
        draw.rectangle([x-size//6, y-size//4, x+size//6, y+size//6], fill=r)
        draw.arc([x-size//3, y-size//8, x+size//3, y+size//3], 0, 180, fill=r, width=3)
        draw.line([x, y+size//3, x, y+size//2], fill=r, width=3)
        draw.line([x-size//4, y+size//2, x+size//4, y+size//2], fill=r, width=3)

    elif icon_type == "graph":
        # Network nodes
        positions = [(x, y-size//3), (x-size//3, y+size//6), (x+size//3, y+size//6),
                     (x-size//5, y-size//6), (x+size//5, y+size//3)]
        # Draw connections
        for i, p1 in enumerate(positions):
            for p2 in positions[i+1:]:
                draw.line([p1, p2], fill=r, width=2)
        # Draw nodes
        for px, py in positions:
            draw.ellipse([px-6, py-6, px+6, py+6], fill=r)

    elif icon_type == "doc":
        # Document with lines
        draw.rectangle([x-size//3, y-size//2, x+size//3, y+size//2], fill=r)
        # Corner fold
        draw.polygon([(x+size//6, y-size//2), (x+size//3, y-size//3), (x+size//6, y-size//3)],
                    fill=hex_to_rgb(CHARCOAL_BG))
        # Lines
        for i in range(3):
            ly = y - size//6 + i * size//5
            draw.line([x-size//5, ly, x+size//5, ly], fill=hex_to_rgb(CHARCOAL_BG), width=2)

    elif icon_type == "canvas":
        # Text editor icon
        draw.rectangle([x-size//2, y-size//2, x+size//2, y+size//2], outline=r, width=2)
        # Text lines
        draw.line([x-size//3, y-size//4, x+size//4, y-size//4], fill=r, width=3)
        draw.line([x-size//3, y, x+size//6, y], fill=r, width=3)
        draw.line([x-size//3, y+size//4, x+size//3, y+size//4], fill=r, width=3)

    elif icon_type == "memory":
        # Brain/neural icon
        draw.ellipse([x-size//2, y-size//3, x+size//2, y+size//3], outline=r, width=2)
        # Neural connections
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            cx = x + int(size//4 * math.cos(rad))
            cy = y + int(size//5 * math.sin(rad))
            draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=r)

    elif icon_type == "gsw":
        # Timeline/temporal icon
        draw.line([x-size//2, y, x+size//2, y], fill=r, width=2)
        draw.polygon([(x+size//2-10, y-8), (x+size//2, y), (x+size//2-10, y+8)], fill=r)
        # Time points
        for i in range(-2, 3):
            px = x + i * size//5
            draw.ellipse([px-5, y-5, px+5, y+5], fill=r)
            draw.line([px, y-5, px, y-size//3], fill=r, width=2)

    elif icon_type == "image":
        # Image/photo icon
        draw.rectangle([x-size//2, y-size//3, x+size//2, y+size//2], outline=r, width=2)
        # Mountain
        draw.polygon([(x-size//3, y+size//3), (x-size//8, y), (x+size//6, y+size//3)], fill=r)
        draw.polygon([(x, y+size//3), (x+size//5, y-size//8), (x+size//2-3, y+size//3)], fill=r)
        # Sun
        draw.ellipse([x+size//5, y-size//5, x+size//3, y-size//12], fill=r)

    elif icon_type == "admin":
        # Gear icon
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            tx = x + int(size//2.5 * math.cos(rad))
            ty = y + int(size//2.5 * math.sin(rad))
            draw.rectangle([tx-5, ty-5, tx+5, ty+5], fill=r)
        draw.ellipse([x-size//4, y-size//4, x+size//4, y+size//4], fill=r)
        draw.ellipse([x-size//8, y-size//8, x+size//8, y+size//8], fill=hex_to_rgb(CARD_BG))

    elif icon_type == "responsive":
        # Devices icon
        # Desktop
        draw.rectangle([x-size//2, y-size//3, x+size//6, y+size//6], outline=r, width=2)
        draw.line([x-size//5, y+size//6, x-size//5, y+size//3], fill=r, width=2)
        draw.line([x-size//3, y+size//3, x-size//12, y+size//3], fill=r, width=2)
        # Mobile
        draw.rectangle([x+size//5, y-size//6, x+size//2, y+size//2], outline=r, width=2)
        draw.ellipse([x+size//3-3, y+size//3, x+size//3+3, y+size//3+6], fill=r)

def create_infographic():
    """Create the main infographic image"""
    # Create image with gradient background
    img = Image.new('RGB', (WIDTH, HEIGHT), hex_to_rgb(CHARCOAL_BG))
    draw = ImageDraw.Draw(img)

    # Add subtle gradient overlay
    for y in range(HEIGHT):
        alpha = int(20 * (1 - y / HEIGHT))
        for x in range(WIDTH):
            if (x + y) % 50 == 0:  # Subtle dot pattern
                current = img.getpixel((x, y))
                img.putpixel((x, y), (current[0] + alpha, current[1] + alpha, current[2] + alpha + 5))

    draw = ImageDraw.Draw(img)

    # Try to load system fonts, fallback to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 56)
        subtitle_font = ImageFont.truetype("arial.ttf", 24)
        feature_title_font = ImageFont.truetype("arialbd.ttf", 18)
        feature_desc_font = ImageFont.truetype("arial.ttf", 13)
        logo_font = ImageFont.truetype("arialbd.ttf", 36)
    except:
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            feature_title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
            feature_desc_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
            logo_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            feature_title_font = ImageFont.load_default()
            feature_desc_font = ImageFont.load_default()
            logo_font = ImageFont.load_default()

    # Draw header area
    # Logo and title
    logo_text = "VERRIDIAN"
    draw.text((80, 50), logo_text, font=logo_font, fill=hex_to_rgb(EMERALD))

    title_text = "LAW OS"
    draw.text((80, 95), title_text, font=title_font, fill=hex_to_rgb(WHITE))

    # Subtitle
    subtitle_text = "AI-Powered Legal Intelligence Platform"
    draw.text((80, 165), subtitle_text, font=subtitle_font, fill=hex_to_rgb(GRAY_TEXT))

    # Decorative line
    draw.line([80, 205, 500, 205], fill=hex_to_rgb(EMERALD), width=3)
    draw.ellipse([495, 200, 510, 215], fill=hex_to_rgb(EMERALD))

    # Version badge
    draw_rounded_rect(draw, [1700, 60, 1840, 95], 15, hex_to_rgb(EMERALD_DARK))
    try:
        badge_font = ImageFont.truetype("arial.ttf", 16)
    except:
        badge_font = feature_desc_font
    draw.text((1720, 68), "v1.0 RELEASE", font=badge_font, fill=hex_to_rgb(WHITE))

    # Draw feature cards
    card_width = 340
    card_height = 160
    padding = 25
    start_x = 80
    start_y = 250
    cards_per_row = 5

    for i, feature in enumerate(FEATURES):
        row = i // cards_per_row
        col = i % cards_per_row

        x = start_x + col * (card_width + padding)
        y = start_y + row * (card_height + padding)

        # Card background with gradient effect
        draw_rounded_rect(draw, [x, y, x + card_width, y + card_height], 12,
                         hex_to_rgb(CARD_BG), hex_to_rgb(CARD_BORDER), 2)

        # Emerald accent line at top of card
        draw.line([x + 15, y + 2, x + 80, y + 2], fill=hex_to_rgb(EMERALD), width=3)

        # Icon
        icon_x = x + 50
        icon_y = y + 60
        draw_icon(draw, feature["icon"], icon_x, icon_y, 50, EMERALD)

        # Feature title
        draw.text((x + 100, y + 40), feature["title"], font=feature_title_font,
                 fill=hex_to_rgb(WHITE))

        # Feature description (wrap text)
        desc = feature["desc"]
        draw.text((x + 100, y + 70), desc, font=feature_desc_font,
                 fill=hex_to_rgb(GRAY_TEXT))

        # Feature number badge
        num_x = x + card_width - 35
        num_y = y + card_height - 35
        draw.ellipse([num_x - 12, num_y - 12, num_x + 12, num_y + 12],
                    fill=hex_to_rgb(EMERALD_DARK))
        try:
            num_font = ImageFont.truetype("arialbd.ttf", 14)
        except:
            num_font = feature_desc_font
        num_text = str(i + 1)
        # Center the number
        bbox = draw.textbbox((0, 0), num_text, font=num_font)
        tw = bbox[2] - bbox[0]
        draw.text((num_x - tw//2, num_y - 8), num_text, font=num_font, fill=hex_to_rgb(WHITE))

    # Footer
    footer_y = HEIGHT - 80
    draw.line([80, footer_y, WIDTH - 80, footer_y], fill=hex_to_rgb(CARD_BORDER), width=1)

    # Footer text
    try:
        footer_font = ImageFont.truetype("arial.ttf", 14)
    except:
        footer_font = feature_desc_font

    draw.text((80, footer_y + 20), "10 Integrated Features", font=footer_font,
             fill=hex_to_rgb(EMERALD))
    draw.text((80, footer_y + 40), "Episodic Memory | Knowledge Graph | Vector Search",
             font=footer_font, fill=hex_to_rgb(GRAY_TEXT))

    # Tech stack badges
    techs = ["Next.js", "FastAPI", "Mem0", "VSA", "TOON"]
    badge_x = WIDTH - 80 - len(techs) * 85
    for tech in techs:
        draw_rounded_rect(draw, [badge_x, footer_y + 25, badge_x + 75, footer_y + 50],
                         10, hex_to_rgb(CARD_BG), hex_to_rgb(EMERALD_DARK), 1)
        bbox = draw.textbbox((0, 0), tech, font=footer_font)
        tw = bbox[2] - bbox[0]
        draw.text((badge_x + 37 - tw//2, footer_y + 32), tech, font=footer_font,
                 fill=hex_to_rgb(EMERALD_GLOW))
        badge_x += 85

    # Decorative elements
    # Corner accents
    draw.line([0, 0, 100, 0], fill=hex_to_rgb(EMERALD), width=4)
    draw.line([0, 0, 0, 100], fill=hex_to_rgb(EMERALD), width=4)
    draw.line([WIDTH, HEIGHT, WIDTH - 100, HEIGHT], fill=hex_to_rgb(EMERALD), width=4)
    draw.line([WIDTH, HEIGHT, WIDTH, HEIGHT - 100], fill=hex_to_rgb(EMERALD), width=4)

    return img

if __name__ == "__main__":
    output_path = r"C:\Users\Danie\Desktop\Fuctional Structure of Episodic Memory\assets\images\LAW_OS_Features_Infographic.png"

    print("Creating Verridian LAW OS Infographic...")
    img = create_infographic()

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the image
    img.save(output_path, "PNG", quality=100)
    print(f"Infographic saved to: {output_path}")
    print(f"Dimensions: {img.width}x{img.height}")
