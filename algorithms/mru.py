from time import perf_counter

from algorithms.leitor_arquivos import ler_arquivo
from algorithms.cache_arquivos import CacheArquivos


def medir_mru(verboso: bool, cache_arquivos: CacheArquivos, id_arquivo: int) -> float:
    """
    Função de medição da performance do MRU. Pode ser usada de
    maneira verbosa ou não verbosa, exibindo ou não o conteúdo do arquivo

        Args:
            verboso (bool): Escolhe entre exibir ou não o conteúdo do arquivo.
            cache_arquivos (CacheArquivos): Cache que será atualizado.
            id_arquivo (int): Arquivo que será inserido no cache.

        Returns:
            float: Tempo que levou para executar 

        Examples:
            >>> medir_mru(True, cache=cache_arquivos, id_arquivo=1)
            0.00238
    """

    tempo_inicio = perf_counter()
    texto = mru(cache_arquivos, id_arquivo)
    if verboso:
        print(f"Conteúdo do arquivo:\n{texto}")
    tempo_fim = perf_counter()
    tempo_total = tempo_fim-tempo_inicio
    return tempo_total


def mru(cache_arquivos: CacheArquivos, id_arquivo: int) -> str:
    """
    Função principal de MRU. Implementada em 3 passos principais::
    1. Verifica se o arquivo está no cache, caso esteja, move o arquivo para o final da lista (Usado Mais Recentemente).
    2. Tenta inserir o arquivo no cache
    3. Caso não consiga inserir, o cache esta cheio. Nesse caso, remove o arquivo último da lista (Usado Mais Recentemente) e tenta novamente

    Args:
        cache_arquivos (list[dict] | None)): Cache que será atualizado.
        id_arquivo (int | None): Arquivo que será inserido no cache.

        Returns:
            str: Texto carregado. 

        Examples:
            >>> cache_arquivos = CacheAwrquivos()
            >>> verifica_cache(cache_arquivos=cache_arquivos, id_arquivo=1)
            'Lore Ipsum ...'
    """

    if not cache_arquivos.contem_arquivo(id_arquivo):
        # arquivo nao esta no cache
        arquivo = ler_arquivo(id_arquivo)

        # Tenta inserir. Se nao conseguir, remove o primero e tenta de novo
        if not cache_arquivos.add_arquivo(id_arquivo, arquivo):
            cache_arquivos.remover_ultimo()
            cache_arquivos.add_arquivo(id_arquivo, arquivo)
    else:
        cache_arquivos.move_para_final(id_arquivo)
        # arquivo estava no cache
        arquivo = cache_arquivos.get_arquivo_pelo_id(
            id_arquivo)  # Pega o arquivo de dentro do cache

    return arquivo

def tests():
    print("="*8, "TESTE MRU", "="*8)

    cache_arquivos_hits = CacheArquivos()
    cache_arquivos_sem_hits = CacheArquivos()

    # 30 números de 1 a 30 -> nenhum hit possível
    arqs_sem_hit = [i for i in range(1,31)]

       # Sequência para testar MRU (30 acessos)
    arqs_com_hit = [
        1,2,3,4,5,6,7,8,9,10,   # Enche o cache (0 hits)
        8,9,10,                 # Hits: movem para "mais recentes" (3 hits)
        11,12,13,               # Inserem novos -> removem o MRU (10,11,12) (misses)
        10,9,8,                 # 10 foi removido (miss), 9 e 8 ainda estão (2 hits)
        1,2,3,                  # Hits (ainda no cache) (3 hits)
        14,15,16,               # Novos, removem os MRUs atuais (misses)
        11,12,13,               # Tentativa de acessar 11-13 
        4,5,6,4                 # Complementam 30 acessos com mais 4 hits
    ]

    tempo_sem_hits = 0.0
    tempo_hits = 0.0

    for arq in arqs_sem_hit:
        tempo_sem_hits += medir_mru(False, cache_arquivos_sem_hits, arq)

    for arq in arqs_com_hit:
        tempo_hits += medir_mru(False, cache_arquivos_hits, arq)

    print(f"Tempo sem hits: {tempo_sem_hits}")
    print(f"Tempo com hits: {tempo_hits}")

    print(f"Hits esperados no caso sem hits: 0\nHits obtidos: {cache_arquivos_sem_hits.get_hits()}")
    print(f"Hits esperados no caso com hits: 8\nHits obtidos: {cache_arquivos_hits.get_hits()}")

    assert (tempo_sem_hits > tempo_hits)
    assert (cache_arquivos_sem_hits.get_hits() == 0)
    assert (cache_arquivos_hits.get_hits() == 12)
