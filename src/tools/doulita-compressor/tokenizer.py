import tiktoken

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """Cuenta tokens en texto usando el tokenizador de OpenAI."""
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError:
        enc = tiktoken.get_encoding("cl100k_base")  # Respaldo seguro
    return len(enc.encode(text))
