from time import perf_counter

from algorithms.leitor_arquivos import ler_arquivo
from algorithms.cache_arquivos import CacheArquivos


def medir_lru(verboso: bool, cache_arquivos: CacheArquivos, id_arquivo: int) -> float:
    """
    Função de medição da performance do LRU. Pode ser usada de
    maneira verbosa ou não verbosa, exibindo ou não o conteúdo do arquivo

        Args:
            verboso (bool): Escolhe entre exibir ou não o conteúdo do arquivo.
            cache_arquivos (CacheArquivos): Cache que será atualizado.
            id_arquivo (int): Arquivo que será inserido no cache.

        Returns:
            float: Tempo que levou para executar 

        Examples:
            >>> medir_lru(True, cache=cache_arquivos, id_arquivo=1)
            0.00238
    """

    tempo_inicio = perf_counter()
    texto = lru(cache_arquivos, id_arquivo)
    if verboso:
        print(f"Conteúdo do arquivo:\n{texto}")
    tempo_fim = perf_counter()
    tempo_total = tempo_fim-tempo_inicio
    return tempo_total


def lru(cache_arquivos: CacheArquivos, id_arquivo: int) -> str:
    """
    Função principal de LRU. Implementada em 3 passos principais::
    1. Verifica se o arquivo está no cache, caso esteja, move o arquivo para o final da lista (Usado Menos Recentemente).
    2. Caso não esteja, tenta inserir o arquivo no cache.
    3. Caso não consiga inserir, o cache esta cheio. Nesse caso, remove o arquivo primeiro da lista (Usado Menos Recentemente) e tenta novamente.

    Args:
        cache_arquivos (CacheArquivos): Cache que será atualizado.
        id_arquivo (int | None): ID do arquivo que será inserido no cache.
        Returns:
            str: Texto carregado
        Examples:
            >>> cache_arquivos = CacheArquivos()
            >>> verifica_cache(cache_arquivos=cache_arquivos, id_arquivo=1)
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
        cache_arquivos.move_para_final(id_arquivo)
        # arquivo estava no cache
        arquivo = cache_arquivos.get_arquivo_pelo_id(
            id_arquivo)  # Pega o arquivo de dentro do cache
    return arquivo


def tests():
    print("="*8, "TESTE LRU", "="*8)
    cache_arquivos_hits = CacheArquivos()
    cache_arquivos_sem_hits = CacheArquivos()

    # 30 números de 1 a 15 -> nenhum hit possível
    arqs_sem_hit = [(i % 15) + 1 for i in range(30)]

    # Sequência para testar LRU
    arqs_com_hit = [
        1,2,3,4,5,6,7,8,9,10,   # Enche cache
        3,5,7,9,                # Rejuvenescem (hits)
        11,12,13,14,15,16,      # Inserem novos (removem menos usados: 1,2,4,6,8,10)
        3,5,7,9,                # Ainda no cache (hits)
        3,5,7,9,3,5,7,9,        # Mais hits
        17,18,19,20             # Novos, removem LRU atuais
    ]

    tempo_sem_hits = 0
    tempo_hits = 0

    for arq in arqs_sem_hit:
        tempo_sem_hits += medir_lru(False, cache_arquivos_sem_hits, arq)

    for arq in arqs_com_hit:
        tempo_hits += medir_lru(False, cache_arquivos_hits, arq)

    print(f"Tempo sem hits: {tempo_sem_hits}")
    print(f"Tempo com hits: {tempo_hits}")

    print(f"Hits esperados no caso sem hits: 0\nHits obtidos: {cache_arquivos_sem_hits.get_hits()}")
    print(f"Hits esperados no caso com hits: 8\nHits obtidos: {cache_arquivos_hits.get_hits()}")

    assert (tempo_sem_hits > tempo_hits)
    assert (cache_arquivos_sem_hits.get_hits() == 0)
    assert (cache_arquivos_hits.get_hits() == 16)
