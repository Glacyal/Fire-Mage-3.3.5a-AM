"""
Implementazione Protocollo AceSerializer-3.0 (Revisione 1)
=========================================================
Serializza strutture dati Python (dizionari, liste, numeri, booleani, stringhe)
nel formato nativo di serializzazione utilizzato dagli addon di World of Warcraft (Ace3).
"""

# Tabella di traduzione precalcolata per escape AceSerializer-3.0
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
    """Serializza ricorsivamente valori Python in formato AceSerializer-3.0."""
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
    raise ValueError(f'Unsupported type for AceSerializer: {type(v)}')


def ace_serialize(obj) -> str:
    """Incapsula un oggetto serializzato con l'header AceSerializer '^1' e il terminatore '^^'."""
    return '^1' + serialize_value(obj) + '^^'
