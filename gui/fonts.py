# Centralized font definitions — MiSans 字体
# main.py 中已通过 AddFontResourceEx 注册 MiSans-Normal.otf

# 字体族名称（OTF 内部注册名）
FONT_FAMILY = "MiSans"
MONO_FAMILY = "Cascadia Code"

# Base multiplier for scaling
BASE = 1

# Primary UI font - MiSans
UI_XS = (FONT_FAMILY, 11 * BASE)
UI_S = (FONT_FAMILY, 12 * BASE)
UI_S_B = (FONT_FAMILY, 12 * BASE, "bold")
UI_M = (FONT_FAMILY, 13 * BASE)
UI_M_B = (FONT_FAMILY, 13 * BASE, "bold")
UI_L = (FONT_FAMILY, 15 * BASE)
UI_L_B = (FONT_FAMILY, 15 * BASE, "bold")
UI_XL = (FONT_FAMILY, 18 * BASE)
UI_XL_B = (FONT_FAMILY, 18 * BASE, "bold")

# Monospace fonts - For console and technical displays
MONO_XS = (MONO_FAMILY, 10 * BASE)
MONO_S = (MONO_FAMILY, 11 * BASE)
MONO_S_B = (MONO_FAMILY, 11 * BASE, "bold")
MONO_M = (MONO_FAMILY, 13 * BASE)
MONO_M_B = (MONO_FAMILY, 13 * BASE, "bold")

# Legacy aliases
CONSOLAS_XS = MONO_XS
CONSOLAS_S = MONO_S
CONSOLAS_M = MONO_M
CONSOLAS_M_B = MONO_M_B
