import math
import random
from waveform_library import get_random_for_second, scale_waveform, loop_waveform, get_preset


def _clamp(value: int, min_val: int = 0, max_val: int = 200) -> int:
    return max(min_val, min(max_val, value))


def _make_entry(freq: int, intensity: int) -> str:
    """Generate FFFFIIII format: 4 freq bytes then 4 intensity bytes."""
    f = _clamp(freq, 0, 255)
    i = _clamp(intensity, 0, 200)
    return f"{f:02X}{f:02X}{f:02X}{f:02X}{i:02X}{i:02X}{i:02X}{i:02X}"


def generate_one_shot(seconds: int, intensity: int) -> list[str]:
    count = seconds * 10
    entry = _make_entry(0x0A, intensity)
    return [entry] * count


def generate_gradual(seconds: int, intensity: int) -> list[str]:
    count = seconds * 10
    entries = []
    for i in range(count):
        t = i / max(count - 1, 1)
        eased = (1 - math.cos(t * math.pi)) / 2
        current = int(intensity * eased)
        current = _clamp(current, 0, intensity)
        entries.append(_make_entry(0x0A, current))
    return entries


def generate_waveform(seconds: int, intensity: int, mode: str = "instant",
                      waveform_mode: str = "library",
                      custom_waveform: str = "") -> list[str]:
    """Generate waveform based on seconds, intensity, and mode.

    waveform_mode:
        "library" - use random preset waveforms from library
        "custom" - use specific preset chosen by user
    """
    seconds = max(1, min(10, seconds))
    intensity = _clamp(intensity)

    if waveform_mode == "library":
        name, preset = get_random_for_second(seconds)
        scaled = scale_waveform(preset, intensity)
        return loop_waveform(scaled, seconds * 10)
    elif waveform_mode == "custom" and custom_waveform:
        preset = get_preset(custom_waveform)
        if preset:
            scaled = scale_waveform(preset, intensity)
            return loop_waveform(scaled, seconds * 10)
    elif mode == "gradual":
        return generate_gradual(seconds, intensity)
    return generate_one_shot(seconds, intensity)


def waveform_to_display_data(entries: list[str]) -> list[int]:
    """Decode FFFFIIII entries into average intensity per entry."""
    result = []
    for entry in entries:
        intensities = []
        for j in range(4):
            pos = 8 + j * 2
            if pos + 2 <= len(entry):
                try:
                    intensities.append(int(entry[pos:pos + 2], 16))
                except ValueError:
                    intensities.append(0)
        result.append(sum(intensities) // max(len(intensities), 1))
    return result


def generate_smooth_feeder_waveform(intensity: int, count: int = 10) -> list[str]:
    """Generate a smooth, continuous waveform chunk for the feeder.
    Uses sine-wave and gradual patterns — no zero-intensity gaps."""
    intensity = _clamp(intensity)
    if intensity == 0:
        return [_make_entry(0x0A, 0)] * count

    # Pick from several smooth patterns that feel different
    pattern_type = random.choice(["sine", "ramp_up", "ramp_down", "triangle", "gentle_pulse"])

    if pattern_type == "sine":
        # Smooth sine wave, never drops to zero
        entries = []
        for i in range(count):
            t = i / max(count, 1)
            val = int(intensity * (0.5 + 0.5 * math.sin(2 * math.pi * t - math.pi / 2)))
            val = max(1, min(intensity, val))
            entries.append(_make_entry(0x0A, val))
        return entries

    elif pattern_type == "ramp_up":
        # Gradual ramp from 30% to full
        entries = []
        for i in range(count):
            t = i / max(count - 1, 1)
            base = int(intensity * 0.3)
            val = int(base + (intensity - base) * t)
            val = max(1, min(intensity, val))
            entries.append(_make_entry(0x0A, val))
        return entries

    elif pattern_type == "ramp_down":
        # Gradual ramp down from full to 30%
        entries = []
        for i in range(count):
            t = i / max(count - 1, 1)
            base = int(intensity * 0.3)
            val = int(intensity - (intensity - base) * t)
            val = max(1, min(intensity, val))
            entries.append(_make_entry(0x0A, val))
        return entries

    elif pattern_type == "triangle":
        # Triangle wave: ramp up then down
        entries = []
        for i in range(count):
            t = i / max(count, 1)
            val = int(intensity * (1 - abs(2 * t - 1)))
            val = max(1, min(intensity, val))
            entries.append(_make_entry(0x0A, val))
        return entries

    else:  # gentle_pulse
        # Gentle pulsing — oscillates between 50% and 100%
        entries = []
        for i in range(count):
            t = i / max(count, 1)
            val = int(intensity * (0.5 + 0.5 * math.sin(2 * math.pi * t)))
            val = max(1, min(intensity, val))
            entries.append(_make_entry(0x0A, val))
        return entries


def generate_ab_waveforms(seconds: int, a_intensity: int, b_intensity: int,
                          mode: str = "instant", waveform_mode: str = "library",
                          alternate: bool = True,
                          custom_waveform: str = "") -> tuple[list[str], list[str], str, str]:
    """Generate waveforms for both A and B channels.
    Returns (a_wave, b_wave, a_preset_name, b_preset_name)
    If alternate=True, A and B use different random presets.
    """
    a_name = ""
    b_name = ""

    if waveform_mode == "library" or waveform_mode == "custom":
        if waveform_mode == "custom" and custom_waveform:
            a_data = get_preset(custom_waveform)
            b_data = get_preset(custom_waveform)
            a_name = custom_waveform
            b_name = custom_waveform
            if not a_data:
                a_data = get_random_for_second(seconds)[1]
                a_name = ""
            if not b_data:
                b_data = get_random_for_second(seconds)[1]
                b_name = ""
        elif alternate:
            a_name, a_data = get_random_for_second(seconds)
            b_name, b_data = get_random_for_second(seconds)
            attempts = 0
            while b_name == a_name and attempts < 5:
                b_name, b_data = get_random_for_second(seconds)
                attempts += 1
        else:
            a_name, a_data = get_random_for_second(seconds)
            b_name = a_name
            b_data = a_data
        a_wave = loop_waveform(scale_waveform(a_data, a_intensity), seconds * 10)
        b_wave = loop_waveform(scale_waveform(b_data, b_intensity), seconds * 10)
    else:
        a_wave = generate_waveform(seconds, a_intensity, mode, waveform_mode)
        b_wave = generate_waveform(seconds, b_intensity, mode, waveform_mode)

    return a_wave, b_wave, a_name, b_name
