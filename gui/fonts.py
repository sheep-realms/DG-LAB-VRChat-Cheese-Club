# Centralized font definitions - Professional typography system

# Base multiplier for scaling
BASE = 2

# Primary UI font - Segoe UI for Windows 11 native feel
UI_XS = ("Segoe UI", 7 * BASE)
UI_S = ("Segoe UI", 8 * BASE)
UI_S_B = ("Segoe UI", 8 * BASE, "bold")
UI_M = ("Segoe UI", 9 * BASE)
UI_M_B = ("Segoe UI", 9 * BASE, "bold")
UI_L = ("Segoe UI", 11 * BASE)
UI_L_B = ("Segoe UI", 11 * BASE, "bold")
UI_XL = ("Segoe UI", 13 * BASE)
UI_XL_B = ("Segoe UI", 13 * BASE, "bold")

# Secondary font - Microsoft YaHei for Chinese characters
YAHEI_XS = ("Microsoft YaHei UI", 7 * BASE)
YAHEI_S = ("Microsoft YaHei UI", 8 * BASE)
YAHEI_S_B = ("Microsoft YaHei UI", 8 * BASE, "bold")
YAHEI_M = ("Microsoft YaHei UI", 9 * BASE)
YAHEI_M_B = ("Microsoft YaHei UI", 9 * BASE, "bold")
YAHEI_L = ("Microsoft YaHei UI", 11 * BASE)
YAHEI_L_B = ("Microsoft YaHei UI", 11 * BASE, "bold")
YAHEI_EMOJI = ("Segoe UI Emoji", 9 * BASE)

# Monospace fonts - For console and technical displays
MONO_XS = ("Cascadia Code", 7 * BASE)
MONO_S = ("Cascadia Code", 8 * BASE)
MONO_S_B = ("Cascadia Code", 8 * BASE, "bold")
MONO_M = ("Cascadia Code", 9 * BASE)
MONO_M_B = ("Cascadia Code", 9 * BASE, "bold")

# Legacy aliases for backward compatibility
CONSOLAS_XS = MONO_XS
CONSOLAS_S = MONO_S
CONSOLAS_M = MONO_M
CONSOLAS_M_B = MONO_M_B
