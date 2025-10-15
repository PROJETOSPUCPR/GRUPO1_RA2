from time import perf_counter

from algorithms.leitor_arquivos import ler_arquivo
from algorithms.cache_arquivos import CacheArquivos


def medir_fifo(verboso: bool, cache_arquivos: CacheArquivos, id_arquivo: int) -> float:
    """
    Função de medição da performance do FIFO. Pode ser usada de
    maneira verbosa ou não verbosa, exibindo ou não o conteúdo do arquivo

        Args:
            verboso (bool): Escolhe entre exibir ou não o conteúdo do arquivo.
            cache_arquivos (CacheArquivos): Cache que será atualizado.
            id_arquivo (int): Arquivo que será inserido no cache.

        Returns:
            float: Tempo que levou para executar 

        Examples:
            >>> medir_fifo(True, cache=cache_arquivos, id_arquivo=1)
            0.00238
    """

    tempo_inicio = perf_counter()

    texto = fifo(cache_arquivos, id_arquivo)
    if verboso and id_arquivo:
        print(f"Conteúdo do arquivo:\n{texto}")
    tempo_fim = perf_counter()
    tempo_total = tempo_fim-tempo_inicio
    return tempo_total


def fifo(cache_arquivos: CacheArquivos, id_arquivo: int) -> str:
    """
    Função principal de FIFO. Implementada em 3 passos principais:
    1. Verifica se o arquivo está no cache.
    2. Caso não esteja. tenta inserir o arquivo no cache.
    3. Caso não consiga inserir, o cache esta cheio. Nesse caso, remove o que foi inserido primeiro (FIFO) e tenta novamente.

    Args:
        cache (list[dict] | None)): Cache que será atualizado.
        bloco (int | None): Arquivo que será inserido no cache.

        Returns:
            str: Texto carregado. 

        Examples:
            >>> cache_arquivos = CacheArquivos()
            >>> fifo(cache_arquivos=cache_arquivos, id_arquivo=1)
            'Lorem Ipsum ...'
    """

    if not cache_arquivos.contem_arquivo(id_arquivo):
        # arquivo nao esta no cache
        arquivo = ler_arquivo(id_arquivo)
        # Tenta inserir. Se nao conseguir, remove o primero e tenta de novo
        if not cache_arquivos.add_arquivo(id_arquivo, arquivo):
            cache_arquivos.remover_primeiro()
            cache_arquivos.add_arquivo(id_arquivo, arquivo)
    else:
        # arquivo estava no cache
        arquivo = cache_arquivos.get_arquivo_pelo_id(
            id_arquivo)  # Pega o arquivo de dentro do cache

    return arquivo


def tests():
    print("="*8, "TESTE FIFO", "="*8)
    cache_arquivos_hits = CacheArquivos()
    cache_arquivos_sem_hits = CacheArquivos()

    # 30 números de 1 a 15 -> nenhum hit possível
    arqs_sem_hit = [(i % 15) + 1 for i in range(30)] 


    # Sequência para testar FIFO
    arqs_com_hit = [
        1,2,3,4,5,6,7,8,9,10,   # Enche o cache
        3,5,7,9,                # Gera hits
        11,12,13,14,15,16,      # Gera substituições (remove 1–6)
        7,8,9,10,7,8,9,10,7,8   # Gera mais 10 hits
    ]

    tempo_sem_hits = 0
    tempo_hits = 0

    for arq in arqs_sem_hit:
        tempo_sem_hits += medir_fifo(False, cache_arquivos_sem_hits, arq)

    for arq in arqs_com_hit:
        tempo_hits += medir_fifo(False, cache_arquivos_hits, arq)

    print(f"Tempo sem hits: {tempo_sem_hits}")
    print(f"Tempo com hits: {tempo_hits}")

    print(f"Hits esperados no caso sem hits: 0\nHits obtidos: {cache_arquivos_sem_hits.get_hits()}")
    print(f"Hits esperados no caso com hits: 8\nHits obtidos: {cache_arquivos_hits.get_hits()}")

    assert (tempo_sem_hits > tempo_hits)
    assert (cache_arquivos_sem_hits.get_hits() == 0)
    assert (cache_arquivos_hits.get_hits() == 14)
