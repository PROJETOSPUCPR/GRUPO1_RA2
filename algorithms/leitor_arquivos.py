def ler_arquivo(arquivo: int):
    return open(f"texts/{arquivo}.txt", 'r', encoding='latin-1').read()