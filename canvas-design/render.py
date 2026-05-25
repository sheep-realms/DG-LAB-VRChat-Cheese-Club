"""Render the Pulse Circuit canvas design — using real waveform library data."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import random
from PIL import Image, ImageDraw, ImageFont
from waveform_library import PRESETS, scale_waveform, loop_waveform
from waveform import waveform_to_display_data

W, H = 1920, 1080
BG = (13, 17, 23)
PANEL = (22, 27, 34)
HEADER = (28, 35, 51)
CYAN = (57, 210, 192)
GREEN = (63, 185, 80)
AMBER = (210, 153, 34)
RED = (248, 81, 73)
PURPLE = (188, 140, 255)
BLUE = (88, 166, 255)
GRID = (33, 38, 45)
TEXT = (230, 237, 243)
TEXT_DIM = (110, 118, 129)
BORDER = (48, 54, 61)

random.seed(42)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

try:
    font_tech = ImageFont.truetype("consola.ttf", 11)
    font_label = ImageFont.truetype("consola.ttf", 13)
    font_title = ImageFont.truetype("consola.ttf", 16)
    font_big = ImageFont.truetype("consola.ttf", 24)
except Exception:
    font_tech = ImageFont.load_default()
    font_label = font_tech
    font_title = font_tech
    font_big = font_tech

# CJK font for Chinese characters
try:
    font_cjk = ImageFont.truetype("msyh.ttc", 11)
    font_cjk_label = ImageFont.truetype("msyh.ttc", 13)
except Exception:
    try:
        font_cjk = ImageFont.truetype("msyhbd.ttc", 11)
        font_cjk_label = ImageFont.truetype("msyhbd.ttc", 13)
    except Exception:
        font_cjk = font_tech
        font_cjk_label = font_label


# ── Decode real waveform data ──────────────────────────────────────────
def decode_entries(hex_entries):
    """Decode hex entries to list of intensity ints (one per 100ms entry)."""
    return waveform_to_display_data(hex_entries)


def decode_to_subframes(hex_entries):
    """Decode hex entries to flat list of intensity ints (one per 25ms sub-frame)."""
    result = []
    for entry in hex_entries:
        for j in range(4):
            pair_start = j * 4
            if pair_start + 4 <= len(entry):
                intensity_hex = entry[pair_start + 2:pair_start + 4]
                try:
                    result.append(int(intensity_hex, 16))
                except ValueError:
                    result.append(0)
    return result


# Pick presets for display
preset_names = list(PRESETS.keys())
ch_a_name = "心跳节奏"
ch_b_name = "压缩"
ch_a_data = scale_waveform(PRESETS[ch_a_name], 200)
ch_b_data = scale_waveform(PRESETS[ch_b_name], 150)
ch_a_looped = loop_waveform(ch_a_data, 100)  # 10 seconds
ch_b_looped = loop_waveform(ch_b_data, 100)

ch_a_entries = decode_entries(ch_a_looped)
ch_b_entries = decode_entries(ch_b_looped)
ch_a_subs = decode_to_subframes(ch_a_looped)
ch_b_subs = decode_to_subframes(ch_b_looped)

# Presets for mini waveforms
mini_presets = ["呼吸", "连击", "波浪涟漪", "渐变弹跳"]
mini_intensities = [100, 120, 150, 180]


# ── Drawing helpers ────────────────────────────────────────────────────
def draw_grid(x0, y0, x1, y1, spacing=20, color=GRID):
    for x in range(x0, x1, spacing):
        draw.line([(x, y0), (x, y1)], fill=color, width=1)
    for y in range(y0, y1, spacing):
        draw.line([(x0, y), (x1, y)], fill=color, width=1)


def draw_step_waveform(x0, y0, x1, y1, values, color, max_val=200, width=2):
    """Draw step-function waveform from decoded intensity values, fitted to bounding box."""
    if not values:
        return
    cy = y1  # bottom of box = 0 intensity
    h = y1 - y0  # total height
    n = len(values)
    step_w = (x1 - x0) / max(n, 1)

    points = []
    for i, v in enumerate(values):
        norm = v / max(max_val, 1)
        py = int(cy - h * norm)
        px = int(x0 + i * step_w)
        points.append((px, py))

    for i in range(len(points) - 1):
        x_a, y_a = points[i]
        x_b, y_b = points[i + 1]
        # Horizontal then vertical (step function)
        draw.line([(x_a, y_a), (x_b, y_a)], fill=color, width=width)
        draw.line([(x_b, y_a), (x_b, y_b)], fill=color, width=width)


def draw_node(x, y, r, color):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=color, outline=color)


def draw_trace(points, color, width=1):
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=color, width=width)


def draw_module(x, y, w, h, title, accent):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=BORDER, width=1)
    draw.rectangle([x, y, x + w, y + 24], fill=HEADER)
    # Use CJK font for titles that may contain Chinese
    f = font_cjk_label if any(ord(c) > 0x2000 for c in title) else font_label
    draw.text((x + 10, y + 5), title, fill=accent, font=f)


# ── BACKGROUND GRID ───────────────────────────────────────────────────
draw_grid(0, 0, W, H, 40, (18, 22, 28))
draw_grid(0, 0, W, H, 200, (25, 30, 38))

# ── CIRCUIT TRACES (decorative background) ────────────────────────────
traces = [
    [(40, 180), (40, 480), (140, 480), (140, 680)],
    [(280, 80), (280, 280), (380, 280), (380, 480)],
    [(480, 780), (480, 580), (580, 580), (580, 380)],
    [(780, 40), (780, 180), (880, 180), (880, 320)],
    [(1080, 880), (1080, 680), (1180, 680), (1180, 480)],
    [(1380, 80), (1380, 220), (1480, 220), (1480, 380)],
    [(1680, 780), (1680, 580), (1780, 580), (1780, 380)],
    [(180, 880), (380, 880), (380, 730)],
    [(980, 80), (1180, 80), (1180, 180)],
    [(1480, 680), (1630, 680), (1630, 530)],
]
trace_colors = [CYAN, GREEN, AMBER, PURPLE, BLUE, RED, CYAN, GREEN, PURPLE, AMBER]
for trace, color in zip(traces, trace_colors):
    draw_trace(trace, color + (50,))

node_positions = [
    (40, 180, CYAN), (140, 480, CYAN), (280, 80, PURPLE),
    (380, 280, PURPLE), (480, 780, AMBER), (580, 580, AMBER),
    (780, 40, BLUE), (880, 180, BLUE), (1080, 880, RED),
    (1180, 680, RED), (1380, 80, CYAN), (1480, 220, CYAN),
    (1680, 780, GREEN), (1780, 580, GREEN),
]
for nx, ny, nc in node_positions:
    draw_node(nx, ny, 3, nc + (100,))

# ── TOP HEADER ────────────────────────────────────────────────────────
draw.rectangle([0, 0, W, 48], fill=HEADER)
draw.line([(0, 48), (W, 48)], fill=CYAN + (50,), width=1)
draw.text((20, 14), "[", fill=CYAN, font=font_title)
draw.text((34, 14), "PULSE CIRCUIT", fill=TEXT, font=font_title)
draw.text((228, 14), "]", fill=CYAN, font=font_title)
draw.text((258, 17), "DG-LAB CONTROL INTERFACE", fill=TEXT_DIM, font=font_tech)
draw.text((W - 120, 17), "v1.2.5", fill=TEXT_DIM, font=font_label)

# ── LEFT COLUMN: Real waveform channels ───────────────────────────────

# Channel A — 心跳节奏 @ 200
draw_module(50, 68, 540, 185, f"CHANNEL A // {ch_a_name}", CYAN)
draw_grid(60, 96, 580, 243, 20, (25, 30, 38))
draw_step_waveform(60, 100, 580, 240, ch_a_entries, CYAN, max_val=200, width=2)
a_peak = max(ch_a_entries) if ch_a_entries else 0
draw.text((60, 246), f"PRESET: {ch_a_name}   PEAK: {a_peak}/200   ENTRIES: {len(ch_a_entries)}", fill=TEXT_DIM, font=font_tech)

# Channel B — 压缩 @ 150
draw_module(50, 272, 540, 185, f"CHANNEL B // {ch_b_name}", AMBER)
draw_grid(60, 300, 580, 447, 20, (25, 30, 38))
draw_step_waveform(60, 304, 580, 444, ch_b_entries, AMBER, max_val=200, width=2)
b_peak = max(ch_b_entries) if ch_b_entries else 0
draw.text((60, 450), f"PRESET: {ch_b_name}   PEAK: {b_peak}/200   ENTRIES: {len(ch_b_entries)}", fill=TEXT_DIM, font=font_tech)

# Combined — both channels overlaid
draw_module(50, 476, 540, 160, "COMBINED OUTPUT // SYNC", GREEN)
draw_grid(60, 504, 580, 626, 20, (25, 30, 38))
draw_step_waveform(60, 508, 580, 622, ch_a_entries, CYAN, max_val=200, width=1)
draw_step_waveform(60, 508, 580, 622, ch_b_entries, AMBER, max_val=200, width=1)

# ── MIDDLE: System Status ─────────────────────────────────────────────
draw_module(620, 68, 420, 250, "SYSTEM STATUS // DIAGNOSTICS", PURPLE)

status_items = [
    ("WEBSOCKET", "CONNECTED", GREEN),
    ("QR PAIRING", "ACTIVE", CYAN),
    ("CHATBOX OSC", "LISTENING :9000", GREEN),
    ("AVATAR OSC", "LISTENING :9001", GREEN),
    ("HTTP SERVER", "READY :8800", GREEN),
    ("WAVEFORM", "STREAMING", AMBER),
    ("STRENGTH A", f"{a_peak} / 200", CYAN),
    ("STRENGTH B", f"{b_peak} / 200", AMBER),
]
for i, (label, value, color) in enumerate(status_items):
    y = 102 + i * 24
    draw.text((640, y), label, fill=TEXT_DIM, font=font_tech)
    draw.ellipse([770, y + 3, 778, y + 11], fill=color)
    draw.text((786, y), value, fill=color, font=font_tech)

# ── MIDDLE: Waveform Monitor — 4 real presets overlaid ────────────────
draw_module(620, 338, 420, 298, "WAVEFORM MONITOR // REAL-TIME", BLUE)
draw_grid(630, 366, 1030, 626, 20, (25, 30, 38))

monitor_presets = ["潮汐", "波浪涟漪", "呼吸", "颗粒摩擦"]
monitor_colors = [BLUE, CYAN, PURPLE, GREEN]
monitor_intensities = [180, 150, 120, 100]
for i, (pname, pcolor, pint) in enumerate(zip(monitor_presets, monitor_colors, monitor_intensities)):
    pdata = scale_waveform(PRESETS[pname], pint)
    plooped = loop_waveform(pdata, 6)  # 6 seconds for monitor
    pentries = decode_entries(plooped)
    inset = i * 6
    draw_step_waveform(630, 374 + inset, 1030, 618 - inset, pentries, pcolor, max_val=200, width=1)

# Time axis
for t in range(7):
    x = 630 + int(t * (400 / 6))
    draw.line([(x, 366), (x, 626)], fill=GRID, width=1)
    draw.text((x - 4, 628), f"{t}s", fill=TEXT_DIM, font=font_tech)

# ── RIGHT COLUMN: QR + Intensity Map + Mini waveforms ─────────────────

# QR Code
qr_x, qr_y = 1070, 68
qr_size = 160
draw.rectangle([qr_x, qr_y, qr_x + qr_size, qr_y + qr_size], fill=PANEL, outline=BORDER)
cell = 7
for r in range(qr_size // cell):
    for c in range(qr_size // cell):
        if random.random() > 0.45 or (r < 3 and c < 3) or (r < 3 and c > qr_size // cell - 4) or (r > qr_size // cell - 4 and c < 3):
            x = qr_x + c * cell
            y = qr_y + r * cell
            draw.rectangle([x, y, x + cell - 1, y + cell - 1], fill=TEXT)
draw.text((qr_x, qr_y + qr_size + 6), "PAIR // SCAN", fill=CYAN, font=font_label)
draw.text((qr_x, qr_y + qr_size + 24), "DG-LAB WEBSOCKET v2", fill=TEXT_DIM, font=font_tech)

# Intensity Map — per-second averages from Channel A (心跳节奏)
bar_x = 1070
bar_y = 310
draw.text((bar_x, bar_y), f"INTENSITY MAP // {ch_a_name}", fill=TEXT, font=font_cjk_label)
# Each second = 10 entries, take the average intensity per second
for sec in range(10):
    start = sec * 10
    end = min(start + 10, len(ch_a_entries))
    if start >= len(ch_a_entries):
        break
    avg = sum(ch_a_entries[start:end]) // max(end - start, 1)
    y = bar_y + 26 + sec * 17
    bar_w = int(avg / 200 * 145)
    draw.rectangle([bar_x, y, bar_x + 145, y + 10], fill=GRID)
    color = CYAN if avg < 100 else AMBER if avg < 180 else RED
    draw.rectangle([bar_x, y, bar_x + bar_w, y + 10], fill=color + (160,))
    draw.text((bar_x + 151, y - 1), f"{sec + 1}s", fill=TEXT_DIM, font=font_tech)
    draw.text((bar_x + 175, y - 1), str(avg), fill=color, font=font_tech)

# Mini waveforms — real presets in 2x2 grid
mini_positions = [
    (1070, 498, 195, 50),
    (1280, 498, 195, 50),
    (1070, 556, 195, 50),
    (1280, 556, 195, 50),
]
mini_colors = [PURPLE, GREEN, AMBER, CYAN]
for (mx, my, mw, mh), pname, pint, mc in zip(mini_positions, mini_presets, mini_intensities, mini_colors):
    draw.rectangle([mx, my, mx + mw, my + mh], fill=PANEL, outline=BORDER)
    pdata = scale_waveform(PRESETS[pname], pint)
    plooped = loop_waveform(pdata, 2)  # 2 seconds
    pentries = decode_entries(plooped)
    draw_step_waveform(mx + 4, my + 5, mx + mw - 4, my + mh - 5, pentries, mc, max_val=200, width=1)

# Mini labels
draw.text((1070, 607), "呼吸", fill=PURPLE + (120,), font=font_cjk)
draw.text((1280, 607), "连击", fill=GREEN + (120,), font=font_cjk)

# ── BOTTOM: Signal Path ───────────────────────────────────────────────
draw_module(50, 660, W - 100, 80, "SIGNAL PATH // DATA FLOW", CYAN)

flow_colors = [CYAN, GREEN, AMBER, PURPLE, BLUE, RED]
seg_w = 52
gap = 7
for i in range(23):
    x = 70 + i * (seg_w + gap)
    h = 16 + random.randint(0, 28)
    color = flow_colors[i % len(flow_colors)]
    y_top = 700 - h // 2
    draw.rectangle([x, y_top, x + seg_w, y_top + h], fill=color + (30,), outline=color + (55,))
    draw.ellipse([x + seg_w // 2 - 2, y_top + h // 2 - 2,
                  x + seg_w // 2 + 2, y_top + h // 2 + 2], fill=color + (180,))

for i in range(21):
    x = 70 + (i + 1) * (seg_w + gap) - gap // 2 - 2
    draw.text((x, 696), ">", fill=TEXT_DIM + (80,), font=font_tech)

annotations = [
    ("NODE", "WEBSERVER:9999"),
    ("PROTOCOL", "PYDGLAB_WS_V2"),
    ("CODEC", "PULSE_OPERATION"),
    ("FRAME", "25MS_INTERVAL"),
    ("BANDWIDTH", "86_ENTRIES_MAX"),
    ("ENCODE", "HEX_INTERLEAVED"),
]
for i, (key, val) in enumerate(annotations):
    x = 70 + i * 290
    y = 750
    draw.text((x, y), f"{key}::", fill=TEXT_DIM + (80,), font=font_tech)
    draw.text((x + len(key) * 7 + 14, y), val, fill=CYAN + (80,), font=font_tech)

# ── BOTTOM STATUS BAR ─────────────────────────────────────────────────
draw.rectangle([0, H - 32, W, H], fill=HEADER)
draw.line([(0, H - 32), (W, H - 32)], fill=CYAN + (50,), width=1)
draw.text((20, H - 24), "芝士郊狼控制软件", fill=TEXT, font=font_cjk_label)
draw.text((220, H - 24), "v1.2.5", fill=TEXT_DIM, font=font_tech)
draw.text((300, H - 24), "//", fill=BORDER, font=font_tech)
draw.text((324, H - 24), "VRChat + DG-LAB", fill=TEXT_DIM, font=font_tech)
draw.text((500, H - 24), "//", fill=BORDER, font=font_tech)
draw.text((524, H - 24), "QQ: 102872939", fill=TEXT_DIM, font=font_tech)
draw.ellipse([W - 170, H - 22, W - 162, H - 14], fill=GREEN)
draw.text((W - 154, H - 24), "ALL SYSTEMS NOMINAL", fill=GREEN, font=font_tech)

# ── ACCENT: vertical separator lines ──────────────────────────────────
draw.line([(605, 68), (605, 640)], fill=BORDER, width=1)
draw.line([(1060, 68), (1060, 700)], fill=BORDER, width=1)

# ── Right-side decorative trace ───────────────────────────────────────
right_trace = [(1480, 238), (1480, 350), (1540, 350), (1540, 460),
               (1600, 460), (1600, 560), (1660, 560), (1660, 620)]
draw_trace(right_trace, GREEN + (35,), width=1)
draw_node(1480, 238, 2, GREEN + (60,))
draw_node(1660, 620, 2, GREEN + (60,))

# ── Save ──────────────────────────────────────────────────────────────
output_path = os.path.join(os.path.dirname(__file__), "pulse_circuit.png")
img.save(output_path, "PNG", quality=95)
print(f"Saved: {output_path} ({img.size[0]}x{img.size[1]})")
