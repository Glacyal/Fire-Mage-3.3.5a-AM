"""
Generatore della Stringa di Importazione WeakAuras (!WA:1!)
===========================================================
Serializza, comprime con Deflate (livello 9) e codifica la tabella dati WeakAuras.
"""
import zlib
from builder.core.serializer import ace_serialize
from builder.core.deflate import libdeflate_encode_for_print


def generate_wa_string(data_table: dict) -> str:
    """
    Serializza, comprime con Deflate (livello 9) e codifica la tabella WeakAuras
    generando la stringa valida per l'import in gioco: '!WA:1!...'.
    
    :param data_table: Struttura dizionario completa dell'albero WeakAuras.
    :return: Stringa di testo pronta da incollare nell'interfaccia di WoW.
    """
    serialized = ace_serialize(data_table)
    comp_obj = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15)
    compressed = comp_obj.compress(serialized.encode('latin1')) + comp_obj.flush()
    encoded = libdeflate_encode_for_print(compressed)
    return f"!WA:1!{encoded}"
