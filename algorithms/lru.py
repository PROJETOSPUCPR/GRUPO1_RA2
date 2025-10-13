from time import time

from algorithms.leitor_arquivos import ler_arquivo
from algorithms.cache_arquivos import CacheArquivos

def lru(dinamico: bool, cache_arquivos: CacheArquivos, blocos: list[int] | None = None, bloco: int | None = None) -> float:

    """
    Função de gerenciamento de cache LRU. Pode ser usada de 
    maneira dinâmica, recebendo um cache e um valor, 
    ou de maneira estática, recebendo um cache e um array de valores.
    No modo Dinâmico, o conteúdo do arquivo será exibido.

        Args:
            dinamico (bool): Escolhe entre estático e dinâmico.
            cache (CacheArquivos): Cache que será atualizado.
            blocos (list[int] | None): Itens que serão inseridos no cache em caso estático. Não é usado em caso dinâmico
            bloco (int | None): Arquivo que será inserido no cache em caso dinâmico. Não é usado em caso estático

        Returns:
            float: Tempo que levou para executar 

        Examples:
            >>> cache_arquivos = CacheArquivos()
            >>> lru(False, cache_arquivos, [1,2,3,4])
            0.00238
            >>> lru(True, cache=cache_arquivos, bloco=1)
            0.00238
    """

    tempo_inicio = time()
    if dinamico and bloco:
        texto = verifica_cache(cache_arquivos, bloco)
        print(f"Primeiras 300 posicoes do texto:\n{texto[:300]}")
    elif blocos:
        for bloco in blocos:
            verifica_cache(cache_arquivos, bloco)
    else:
        raise ValueError("Argumentos inválidos/faltado.")
    tempo_fim = time()
    tempo_total = tempo_fim-tempo_inicio
    return tempo_total

def verifica_cache(cache_arquivos: CacheArquivos, id_arquivo: int) -> str:
    """
    Função auxiliar para verificar o cache. Faz principalmente 3 coisas:
    1. Verifica se o arquivo está no cache, caso esteja, move o arquivo para o fim da lista.
    2. Caso não esteja, tenta inserir o arquivo no cache
    3. Caso não consiga inserir, o cache esta cheio. Nesse caso, remove o arquivo que esta a mais tempo e tenta novamente

    Args:
        cache (list[dict] | None)): Cache que será atualizado.
        bloco (int | None): Arquivo que será inserido no cache.
        Returns:
            str: Texto carregado
        Examples:
            >>> cache_arquivos = CacheArquivos()
            >>> verifica_cache(cache=cache_arquivos, bloco=1, 10)
            'Lore Ipsum ...'

    """
    cache_arquivos.inc_requests()  # aumenta o contador de requisicoes ao cache
    if not cache_arquivos.contem_arquivo(id_arquivo):
        # arquivo nao esta no cache
        arquivo = ler_arquivo(id_arquivo)
        # Tenta inserir. Se nao conseguir, remove o primero e tenta de novo
        if not cache_arquivos.add_arquivo(id_arquivo, arquivo):
            cache_arquivos.remover_primeiro()
            cache_arquivos.add_arquivo(id_arquivo, arquivo)
    else:
        cache_arquivos.move_para_final(id_arquivo)
        # arquivo estava no cache
        arquivo = cache_arquivos.get_arquivo_pelo_id(id_arquivo)  # Pega o arquivo de dentro do cache
        cache_arquivos.inc_hits()
    return arquivo


