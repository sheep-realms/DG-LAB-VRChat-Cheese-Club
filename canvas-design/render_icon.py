"""Render app icon v2: clean geometric coyote with electric bolts."""
import math
from PIL import Image, ImageDraw, ImageFilter
import os

SIZE = 512
BG = (26, 26, 46)
YELLOW = (255, 215, 0)
BLUE = (0, 191, 255)
DARK_BLUE = (0, 100, 160)
DARK_YELLOW = (160, 130, 0)
WHITE = (255, 255, 255)

img = Image.new("RGBA", (SIZE, SIZE), BG + (255,))

# Work on a separate layer for the glow
glow_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_layer)

draw = ImageDraw.Draw(img)
cx, cy = SIZE // 2, SIZE // 2 + 10

# ── Background: subtle radial gradient ─────────────────────────────
for r in range(200, 0, -1):
    alpha = int(15 * (1 - r / 200))
    glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 100, 180, alpha))

# ── Coyote head: clean angular silhouette ─────────────────────────
# Simplified geometric head - single clean shape, not faceted

# The coyote head as a clean angular path
# Top of head -> ears -> sides -> jaw -> chin -> back up
head_points = [
    # Left ear (tall, pointed)
    (cx - 30, cy - 50),   # inner ear base left
    (cx - 80, cy - 160),  # ear tip left
    (cx - 110, cy - 70),  # outer ear base left
    # Left side of head
    (cx - 115, cy - 20),  # temple
    (cx - 100, cy + 40),  # cheek
    (cx - 65, cy + 80),   # jaw
    # Chin
    (cx, cy + 110),
    # Right side (mirror)
    (cx + 65, cy + 80),
    (cx + 100, cy + 40),
    (cx + 115, cy - 20),
    # Right ear
    (cx + 110, cy - 70),
    (cx + 80, cy - 160),
    (cx + 30, cy - 50),
    # Top of head
    (cx, cy - 70),
]

# Fill head with gradient-like effect using multiple overlapping shapes
# Main head fill
draw.polygon(head_points, fill=DARK_YELLOW)

# Lighter inner area
inner_scale = 0.75
inner_points = []
for px, py in head_points:
    ix = cx + (px - cx) * inner_scale
    iy = cy + (py - cy) * inner_scale
    inner_points.append((ix, iy))
draw.polygon(inner_points, fill=YELLOW)

# Bright center highlight
highlight_points = []
for px, py in head_points:
    ix = cx + (px - cx) * 0.5
    iy = cy + (py - cy) * 0.5
    highlight_points.append((ix, iy))
draw.polygon(highlight_points, fill=(255, 230, 50))

# ── Head outline: clean electric blue ──────────────────────────────
for i in range(len(head_points)):
    p1 = head_points[i]
    p2 = head_points[(i + 1) % len(head_points)]
    draw.line([p1, p2], fill=BLUE, width=4)

# ── Eyes: sharp angular diamonds ───────────────────────────────────
eye_size = 20
for side in [-1, 1]:
    ex = cx + side * 52
    ey = cy - 25
    # Outer diamond
    pts = [
        (ex, ey - eye_size),
        (ex + side * 14, ey),
        (ex, ey + eye_size * 0.6),
        (ex - side * 14, ey),
    ]
    draw.polygon(pts, fill=BLUE)
    # Inner bright core
    core = [
        (ex, ey - eye_size * 0.5),
        (ex + side * 7, ey),
        (ex, ey + eye_size * 0.3),
        (ex - side * 7, ey),
    ]
    draw.polygon(core, fill=WHITE)

# ── Nose: clean triangle ───────────────────────────────────────────
draw.polygon([
    (cx, cy + 10),
    (cx - 10, cy + 28),
    (cx + 10, cy + 28),
], fill=BLUE)

# ── Lightning bolts: clean geometric zigzag ────────────────────────
def draw_bolt(draw, x1, y1, x2, y2, color, width=5):
    """Draw a clean lightning bolt between two points."""
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    # Main bolt: 3 segments with offsets
    mid1 = (mx - 20, my - 30)
    mid2 = (mx + 20, my + 10)
    points = [(x1, y1), mid1, mid2, (x2, y2)]
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=color, width=width)

# Left bolt - large
draw_bolt(draw, cx - 130, cy - 120, cx - 160, cy + 60, BLUE, 5)
# Left bolt - small accent
draw_bolt(draw, cx - 155, cy - 50, cx - 175, cy + 30, DARK_BLUE, 3)

# Right bolt - large
draw_bolt(draw, cx + 130, cy - 120, cx + 160, cy + 60, BLUE, 5)
# Right bolt - small accent
draw_bolt(draw, cx + 155, cy - 50, cx + 175, cy + 30, DARK_BLUE, 3)

# ── Electric arcs on forehead ──────────────────────────────────────
arc_color = BLUE
# Small zigzag marks
for dx in [-20, 0, 20]:
    pts = [
        (cx + dx - 5, cy - 60),
        (cx + dx + 5, cy - 50),
        (cx + dx - 5, cy - 40),
    ]
    draw.line(pts, fill=arc_color, width=2)

# ── Cheese wedge: top-right corner ─────────────────────────────────
# Clean triangular cheese with holes
cheese_x, cheese_y = SIZE - 80, 25
cheese_size = 50
cheese_pts = [
    (cheese_x, cheese_y),
    (cheese_x + cheese_size, cheese_y),
    (cheese_x + cheese_size, cheese_y + cheese_size),
]
draw.polygon(cheese_pts, fill=YELLOW)
# Cheese holes (circles)
holes = [(cheese_x + 35, cheese_y + 15, 5), (cheese_x + 20, cheese_y + 35, 4), (cheese_x + 40, cheese_y + 38, 3)]
for hx, hy, hr in holes:
    draw.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=BG)

# ── Border ring ───────────────────────────────────────────────────
border_r = SIZE // 2 - 6
draw.ellipse([cx - border_r, cy - border_r, cx + border_r, cy + border_r],
             outline=BLUE, width=3)
# Inner ring
border_r2 = SIZE // 2 - 12
draw.ellipse([cx - border_r2, cy - border_r2, cx + border_r2, cy + border_r2],
             outline=DARK_BLUE, width=1)

# ── Composite glow layer ──────────────────────────────────────────
glow_blurred = glow_layer.filter(ImageFilter.GaussianBlur(radius=8))
img = Image.alpha_composite(img, glow_blurred)

# ── Save ──────────────────────────────────────────────────────────
output_ico = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app_icon.ico")
output_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app_icon.png")

img.save(output_png, "PNG")
print(f"Saved PNG: {output_png}")

# ICO with multiple sizes
sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
img.save(output_ico, format="ICO", sizes=sizes)
print(f"Saved ICO: {output_ico}")
