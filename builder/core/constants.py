"""
Costanti Globali & Configurazioni di Base per WeakAuras Suite
============================================================
Contiene le costanti di caricamento per Mago Fuoco 3.3.5a e le impostazioni
grafiche condivise (font, texture, colori).
"""

# Condizioni di Caricamento (Load Conditions):
# Classe Mago (Class: MAGE) e talento Living Bomb (Talent ID: 68 - Ramo Fuoco)
FIRE_MAGE_LOAD = {
    "use_class": True,
    "class": {"single": "MAGE", "multi": {"MAGE": True}},
    "use_talent": True,
    "talent": {"single": 68, "multi": {68: True}},
    "use_vehicle": False,
}

# Tipografia e Texture Standard
FONT_EXPRESSWAY = "Expressway"
TEXTURE_STATUSBAR = "Interface\\TargetingFrame\\UI-StatusBar"
TEXTURE_WHITE8X8 = "Interface\\Buttons\\WHITE8X8"
