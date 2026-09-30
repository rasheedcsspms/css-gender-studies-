"""Palette, fonts and the box/card vocabulary shared by every Gender Studies document."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # gs_build/
REPO = ROOT.parent                                   # repository root
FONT_DIR = ROOT / "fonts"
CACHE = ROOT / ".cache"
SUBJECT_DIR = REPO / "CSS Gender Studies"

# ---- colours (hex without '#') -------------------------------------------
PLUM = "6B2D5C"      # the subject colour (MA, cover, H1)
TEAL = "0F766E"
NAVY = "1E2A44"
ROSE = "B83280"
GOLD = "A16207"
BLUE = "2B5C9E"
GREEN = "2F7D4F"
CORAL = "C2410C"
RED = "B91C1C"
SLATE = "475569"
GREY = "94A3B8"
INK = "1F2937"

# one colour per topic (T1..T7); index 0 is the Master Anatomy
TOPIC_COLOURS = [PLUM, TEAL, ROSE, GOLD, BLUE, GREEN, CORAL, NAVY]


def tint(hexcol: str, amount: float = 0.88) -> str:
    """Mix a colour with white. amount=0.88 -> a very pale tint."""
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (round(c + (255 - c) * amount) for c in (r, g, b))
    return f"{r:02X}{g:02X}{b:02X}"


def rgb(hexcol: str):
    return tuple(int(hexcol[i:i + 2], 16) / 255 for i in (0, 2, 4))


# ---- Word fonts -------------------------------------------------------------
BODY_FONT = "Calibri"
HEAD_FONT = "Calibri"
BODY_SIZE = 11

# ---- boxes: (label, colour) -------------------------------------------------
BOXES = {
    "simple":   ("IN SIMPLE WORDS", TEAL),
    "example":  ("EXAMPLE", BLUE),
    "trap":     ("TRAP", RED),
    "eye":      ("EXAMINER'S EYE", NAVY),
    "debate":   ("HOT DEBATE", ROSE),
    "pakistan": ("PAKISTAN ANGLE", GREEN),
    "remember": ("REMEMBER", GOLD),
    "balance":  ("BALANCED VIEW", SLATE),
    "islam":    ("ISLAMIC PERSPECTIVE", "166534"),
    "note":     ("NOTE", SLATE),
    "glance":   ("AT A GLANCE", PLUM),
    "update":   ("LATEST UPDATE", CORAL),
    "method":   ("METHOD", TEAL),
}

# ---- evidence cards: (label, colour) — cards sit INSIDE the point they prove -
CARDS = {
    "define":  ("DEFINITION", TEAL),
    "thinker": ("THINKER", PLUM),
    "quote":   ("QUOTATION", ROSE),
    "data":    ("DATA", BLUE),
    "law":     ("LAW & POLICY", NAVY),
    "case":    ("CASE", CORAL),
    "report":  ("REPORT", GOLD),
}
