"""
Fire Mage 3.3.5a AM WeakAuras Suite Generator (WoW 3.3.5a - WeakAuras 4.0.0 Backport)
================================================================================
Generatore deterministico della stringa di importazione WeakAuras (!WA:1!) per la
suite Fire Mage Livello 80 in World of Warcraft 3.3.5a (Wrath of the Lich King).

Caratteristiche Architetturali:
- Engine Target: WeakAuras 4.0.0 (internalVersion 52) con supporto subRegions native.
- Formato di Codifica: AceSerializer-3.0 Protocol Rev 1 + Deflate compressione zlib
  + LibDeflate Little-Endian 6-bit Base64 encoding.
- Gerarchia Rigorosa: Tutti i moduli sono nidificati sotto il gruppo master "Fire Mage 3.3.5a AM"
  per consentire spostamenti in blocco o disinstallazione pulita con un solo clic.
- Condizione di Caricamento: Classe Mago (Player Class: Mage) e talento Living Bomb (Fire),
  impostato su tutti i nodi foglia per conformità all'engine 3.3.5a.
- Tracciamento Cooldown Avanzato: ICD (Internal Cooldown) software per Trinket e Mantello,
  timer a orologio (cooldown swipe) e allerta rossa numerica (|cFFFF4444%.1fs|r) su tutti i proc.
- Layout Ergonomico: Barre centrali da 264px (+20%), colonna buff a sinistra (x = -182),
  fila utility a 6 icone simmetriche a y = -54.
"""
import zlib

true = True
false = False

CHARS = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
    'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
    'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
    'W', 'X', 'Y', 'Z', '0', '1', '2', '3',
    '4', '5', '6', '7', '8', '9', '(', ')'
]

# Tabella di traduzione precalcolata per escape AceSerializer-3.0 (C-level str.translate)
ACE_ESCAPE_TRANS = {
    30: '~z',
    94: '~}',
    126: '~|',
    127: '~{',
}
for _n in range(33):
    if _n != 30:
        ACE_ESCAPE_TRANS[_n] = '~' + chr(_n + 64)

def serialize_string(s: str) -> str:
    """Serializza una stringa nel formato AceSerializer-3.0 con sequenze di escape per caratteri di controllo."""
    res = ['^S']
    for ch in s:
        n = ord(ch)
        if n == 30:
            res.append('~z')
        elif n <= 32:
            res.append('~' + chr(n + 64))
        elif n == 94:
            res.append('~}')
        elif n == 126:
            res.append('~|')
        elif n == 127:
            res.append('~{')
        else:
            res.append(ch)
    return ''.join(res)

def serialize_value(v) -> str:
    """Serializza ricorsivamente valori Python (None, bool, int/float, str, dict, list) in formato AceSerializer."""
    if v is None:
        return '^Z'
    elif isinstance(v, bool):
        return '^B' if v else '^b'
    elif isinstance(v, (int, float)):
        if isinstance(v, float) and v.is_integer():
            return f'^N{int(v)}'
        return f'^N{v}'
    elif isinstance(v, str):
        return serialize_string(v)
    elif isinstance(v, dict):
        res = ['^T']
        for k, val in v.items():
            res.append(serialize_value(k))
            res.append(serialize_value(val))
        res.append('^t')
        return ''.join(res)
    elif isinstance(v, list):
        res = ['^T']
        for i, val in enumerate(v, 1):
            res.append(serialize_value(i))
            res.append(serialize_value(val))
        res.append('^t')
        return ''.join(res)
    raise ValueError(f'Unsupported type: {type(v)}')

def ace_serialize(obj) -> str:
    """Incapsula un oggetto serializzato con l'header AceSerializer '^1' e il terminatore '^^'."""
    return '^1' + serialize_value(obj) + '^^'

def libdeflate_encode_for_print(data: bytes) -> str:
    """Codifica un buffer binario compresso secondo l'alfabeto personalizzato a 64 caratteri di LibDeflate."""
    n = len(data)
    i = 0
    buffer = []
    while i <= n - 3:
        x1, x2, x3 = data[i], data[i+1], data[i+2]
        i += 3
        cache = x1 + (x2 << 8) + (x3 << 16)
        b1 = cache % 64
        cache = (cache - b1) // 64
        b2 = cache % 64
        cache = (cache - b2) // 64
        b3 = cache % 64
        b4 = (cache - b3) // 64
        buffer.append(CHARS[b1] + CHARS[b2] + CHARS[b3] + CHARS[b4])
    
    cache = 0
    cache_bitlen = 0
    while i < n:
        x = data[i]
        cache += x * (1 << cache_bitlen)
        cache_bitlen += 8
        i += 1
    
    while cache_bitlen > 0:
        bit6 = cache % 64
        buffer.append(CHARS[bit6])
        cache = (cache - bit6) // 64
        cache_bitlen -= 6
    
    return ''.join(buffer)

def generate_wa_string(data_table: dict) -> str:
    """Serializza, comprime con Deflate (livello 9) e codifica la tabella WeakAuras generando la stringa '!WA:1!'."""
    serialized = ace_serialize(data_table)
    comp_obj = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15)
    compressed = comp_obj.compress(serialized.encode('latin1')) + comp_obj.flush()
    encoded = libdeflate_encode_for_print(compressed)
    return f"!WA:1!{encoded}"

