import hashlib

def convertir_texto(texto: str) -> str:
    h = hashlib.new("SHA256")
    h.update(texto.encode())

    return h.hexdigest()


def verificar_texto(texto: str, texto_real: str) -> bool:
    h = hashlib.new("SHA256")
    h.update(texto.encode())

    texto_hash = h.hexdigest()

    if texto_hash == texto_real:
        return True
    return False


texto = "admin"
texto_hash = convertir_texto(texto=texto)

print(texto_hash)
