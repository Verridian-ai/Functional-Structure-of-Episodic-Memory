"""
Verridian LAW OS Features Infographic Generator v2
Enhanced version with statistics and filled layout
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

# Stats data
STATS = [
    {"value": "5,000+", "label": "Knowledge Nodes"},
    {"value": "100K+", "label": "Legal Citations"},
    {"value": "99.9%", "label": "Uptime"},
    {"value": "<100ms", "label": "Response Time"},
]

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def draw_rounded_rect(draw, coords, radius, fill, outline=None, width=1):
    """Draw a rounded rectangle"""
    x1, y1, x2, y2 = coords
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
    draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)
    if outline:
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
        draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//3], fill=r)
        draw.polygon([(x-size//4, y+size//4), (x-size//2, y+size//2), (x, y+size//4)], fill=r)
        draw.ellipse([x+size//4, y-size//4, x+size//2+5, y], fill=r)

    elif icon_type == "voice":
        draw.ellipse([x-size//6, y-size//2, x+size//6, y], fill=r)
        draw.rectangle([x-size//6, y-size//4, x+size//6, y+size//6], fill=r)
        draw.arc([x-size//3, y-size//8, x+size//3, y+size//3], 0, 180, fill=r, width=3)
        draw.line([x, y+size//3, x, y+size//2], fill=r, width=3)
        draw.line([x-size//4, y+size//2, x+size//4, y+size//2], fill=r, width=3)

    elif icon_type == "graph":
        positions = [(x, y-size//3), (x-size//3, y+size//6), (x+size//3, y+size//6),
                     (x-size//5, y-size//6), (x+size//5, y+size//3)]
        for i, p1 in enumerate(positions):
            for p2 in positions[i+1:]:
                draw.line([p1, p2], fill=r, width=2)
        for px, py in positions:
            draw.ellipse([px-6, py-6, px+6, py+6], fill=r)

    elif icon_type == "doc":
        draw.rectangle([x-size//3, y-size//2, x+size//3, y+size//2], fill=r)
        draw.polygon([(x+size//6, y-size//2), (x+size//3, y-size//3), (x+size//6, y-size//3)],
                    fill=hex_to_rgb(CHARCOAL_BG))
        for i in range(3):
            ly = y - size//6 + i * size//5
            draw.line([x-size//5, ly, x+size//5, ly], fill=hex_to_rgb(CHARCOAL_BG), width=2)

    elif icon_type == "canvas":
        draw.rectangle([x-size//2, y-size//2, x+size//2, y+size//2], outline=r, width=2)
        draw.line([x-size//3, y-size//4, x+size//4, y-size//4], fill=r, width=3)
        draw.line([x-size//3, y, x+size//6, y], fill=r, width=3)
        draw.line([x-size//3, y+size//4, x+size//3, y+size//4], fill=r, width=3)

    elif icon_type == "memory":
        draw.ellipse([x-size//2, y-size//3, x+size//2, y+size//3], outline=r, width=2)
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            cx = x + int(size//4 * math.cos(rad))
            cy = y + int(size//5 * math.sin(rad))
            draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=r)

    elif icon_type == "gsw":
        draw.line([x-size//2, y, x+size//2, y], fill=r, width=2)
        draw.polygon([(x+size//2-10, y-8), (x+size//2, y), (x+size//2-10, y+8)], fill=r)
        for i in range(-2, 3):
            px = x + i * size//5
            draw.ellipse([px-5, y-5, px+5, y+5], fill=r)
            draw.line([px, y-5, px, y-size//3], fill=r, width=2)

    elif icon_type == "image":
        draw.rectangle([x-size//2, y-size//3, x+size//2, y+size//2], outline=r, width=2)
        draw.polygon([(x-size//3, y+size//3), (x-size//8, y), (x+size//6, y+size//3)], fill=r)
        draw.polygon([(x, y+size//3), (x+size//5, y-size//8), (x+size//2-3, y+size//3)], fill=r)
        draw.ellipse([x+size//5, y-size//5, x+size//3, y-size//12], fill=r)

    elif icon_type == "admin":
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            tx = x + int(size//2.5 * math.cos(rad))
            ty = y + int(size//2.5 * math.sin(rad))
            draw.rectangle([tx-5, ty-5, tx+5, ty+5], fill=r)
        draw.ellipse([x-size//4, y-size//4, x+size//4, y+size//4], fill=r)
        draw.ellipse([x-size//8, y-size//8, x+size//8, y+size//8], fill=hex_to_rgb(CARD_BG))

    elif icon_type == "responsive":
        draw.rectangle([x-size//2, y-size//3, x+size//6, y+size//6], outline=r, width=2)
        draw.line([x-size//5, y+size//6, x-size//5, y+size//3], fill=r, width=2)
        draw.line([x-size//3, y+size//3, x-size//12, y+size//3], fill=r, width=2)
        draw.rectangle([x+size//5, y-size//6, x+size//2, y+size//2], outline=r, width=2)
        draw.ellipse([x+size//3-3, y+size//3, x+size//3+3, y+size//3+6], fill=r)

def create_infographic():
    """Create the main infographic image"""
    img = Image.new('RGB', (WIDTH, HEIGHT), hex_to_rgb(CHARCOAL_BG))
    draw = ImageDraw.Draw(img)

    # Subtle background pattern
    for y in range(0, HEIGHT, 30):
        for x in range(0, WIDTH, 30):
            alpha = 8
            current = img.getpixel((x, y))
            img.putpixel((x, y), (current[0] + alpha, current[1] + alpha, current[2] + alpha))

    draw = ImageDraw.Draw(img)

    # Load fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 52)
        subtitle_font = ImageFont.truetype("arial.ttf", 22)
        feature_title_font = ImageFont.truetype("arialbd.ttf", 16)
        feature_desc_font = ImageFont.truetype("arial.ttf", 12)
        logo_font = ImageFont.truetype("arialbd.ttf", 32)
        stat_value_font = ImageFont.truetype("arialbd.ttf", 28)
        stat_label_font = ImageFont.truetype("arial.ttf", 12)
        badge_font = ImageFont.truetype("arial.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = title_font
        feature_title_font = title_font
        feature_desc_font = title_font
        logo_font = title_font
        stat_value_font = title_font
        stat_label_font = title_font
        badge_font = title_font

    # Header
    draw.text((60, 35), "VERRIDIAN", font=logo_font, fill=hex_to_rgb(EMERALD))
    draw.text((60, 72), "LAW OS", font=title_font, fill=hex_to_rgb(WHITE))
    draw.text((60, 130), "AI-Powered Legal Intelligence Platform", font=subtitle_font, fill=hex_to_rgb(GRAY_TEXT))

    # Decorative line
    draw.line([60, 165, 380, 165], fill=hex_to_rgb(EMERALD), width=3)
    draw.ellipse([375, 160, 390, 175], fill=hex_to_rgb(EMERALD))

    # Version badge
    draw_rounded_rect(draw, [1720, 45, 1860, 78], 15, hex_to_rgb(EMERALD_DARK))
    draw.text((1745, 52), "v1.0 RELEASE", font=badge_font, fill=hex_to_rgb(WHITE))

    # Feature cards - 2 rows of 5
    card_width = 345
    card_height = 140
    padding = 18
    start_x = 60
    start_y = 195
    cards_per_row = 5

    for i, feature in enumerate(FEATURES):
        row = i // cards_per_row
        col = i % cards_per_row

        x = start_x + col * (card_width + padding)
        y = start_y + row * (card_height + padding)

        # Card background
        draw_rounded_rect(draw, [x, y, x + card_width, y + card_height], 10,
                         hex_to_rgb(CARD_BG), hex_to_rgb(CARD_BORDER), 1)

        # Emerald accent
        draw.line([x + 12, y + 2, x + 70, y + 2], fill=hex_to_rgb(EMERALD), width=3)

        # Icon
        icon_x = x + 45
        icon_y = y + 55
        draw_icon(draw, feature["icon"], icon_x, icon_y, 45, EMERALD)

        # Title and description
        draw.text((x + 90, y + 35), feature["title"], font=feature_title_font, fill=hex_to_rgb(WHITE))
        draw.text((x + 90, y + 60), feature["desc"], font=feature_desc_font, fill=hex_to_rgb(GRAY_TEXT))

        # Number badge
        num_x = x + card_width - 30
        num_y = y + card_height - 30
        draw.ellipse([num_x - 11, num_y - 11, num_x + 11, num_y + 11], fill=hex_to_rgb(EMERALD_DARK))
        num_text = str(i + 1)
        bbox = draw.textbbox((0, 0), num_text, font=badge_font)
        tw = bbox[2] - bbox[0]
        draw.text((num_x - tw//2, num_y - 8), num_text, font=badge_font, fill=hex_to_rgb(WHITE))

    # Statistics section
    stats_y = 530
    draw.text((60, stats_y), "Platform Statistics", font=subtitle_font, fill=hex_to_rgb(WHITE))
    draw.line([60, stats_y + 35, 280, stats_y + 35], fill=hex_to_rgb(EMERALD), width=2)

    stat_width = 200
    stat_padding = 15
    stat_start_x = 60

    for i, stat in enumerate(STATS):
        sx = stat_start_x + i * (stat_width + stat_padding)
        sy = stats_y + 55

        # Stat card
        draw_rounded_rect(draw, [sx, sy, sx + stat_width, sy + 90], 8,
                         hex_to_rgb(CARD_BG), hex_to_rgb(CARD_BORDER), 1)

        # Value
        draw.text((sx + 15, sy + 15), stat["value"], font=stat_value_font, fill=hex_to_rgb(EMERALD_GLOW))
        # Label
        draw.text((sx + 15, sy + 55), stat["label"], font=stat_label_font, fill=hex_to_rgb(GRAY_TEXT))

    # Architecture section
    arch_x = 920
    arch_y = stats_y
    draw.text((arch_x, arch_y), "Architecture Highlights", font=subtitle_font, fill=hex_to_rgb(WHITE))
    draw.line([arch_x, arch_y + 35, arch_x + 280, arch_y + 35], fill=hex_to_rgb(EMERALD), width=2)

    highlights = [
        "TOON Format - Triple-Object-Oriented Notation",
        "VSA Encoding - Vector Symbolic Architecture",
        "Temporal Episodic Memory (TEM)",
        "Force-directed 3D Knowledge Graph",
        "Real-time AI Streaming Pipeline"
    ]

    for i, highlight in enumerate(highlights):
        hy = arch_y + 55 + i * 28
        draw.ellipse([arch_x, hy + 3, arch_x + 8, hy + 11], fill=hex_to_rgb(EMERALD))
        draw.text((arch_x + 18, hy), highlight, font=feature_desc_font, fill=hex_to_rgb(LIGHT_GRAY))

    # Footer
    footer_y = HEIGHT - 65
    draw.line([60, footer_y, WIDTH - 60, footer_y], fill=hex_to_rgb(CARD_BORDER), width=1)

    draw.text((60, footer_y + 15), "10 Integrated Features", font=badge_font, fill=hex_to_rgb(EMERALD))
    draw.text((60, footer_y + 35), "Episodic Memory | Knowledge Graph | Vector Search | AI Generation",
             font=stat_label_font, fill=hex_to_rgb(GRAY_TEXT))

    # Tech stack badges
    techs = ["Next.js", "FastAPI", "Mem0", "VSA", "TOON", "Three.js"]
    badge_x = WIDTH - 60 - len(techs) * 80
    for tech in techs:
        draw_rounded_rect(draw, [badge_x, footer_y + 18, badge_x + 70, footer_y + 43],
                         8, hex_to_rgb(CARD_BG), hex_to_rgb(EMERALD_DARK), 1)
        bbox = draw.textbbox((0, 0), tech, font=stat_label_font)
        tw = bbox[2] - bbox[0]
        draw.text((badge_x + 35 - tw//2, footer_y + 25), tech, font=stat_label_font,
                 fill=hex_to_rgb(EMERALD_GLOW))
        badge_x += 80

    # Corner accents
    draw.line([0, 0, 80, 0], fill=hex_to_rgb(EMERALD), width=4)
    draw.line([0, 0, 0, 80], fill=hex_to_rgb(EMERALD), width=4)
    draw.line([WIDTH-1, HEIGHT-1, WIDTH - 81, HEIGHT-1], fill=hex_to_rgb(EMERALD), width=4)
    draw.line([WIDTH-1, HEIGHT-1, WIDTH-1, HEIGHT - 81], fill=hex_to_rgb(EMERALD), width=4)

    return img

if __name__ == "__main__":
    output_path = r"C:\Users\Danie\Desktop\Fuctional Structure of Episodic Memory\assets\images\LAW_OS_Features_Infographic.png"

    print("Creating Verridian LAW OS Infographic v2...")
    img = create_infographic()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", quality=100)
    print(f"Infographic saved to: {output_path}")
    print(f"Dimensions: {img.width}x{img.height}")
