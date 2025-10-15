from time import perf_counter
from algorithms.leitor_arquivos import ler_arquivo
from algorithms.cache_arquivos import CacheArquivos

# Dicionário para rastrear a frequência de cada arquivo no cache.
# Ele será passado junto com o cache para a função.
frequencia_acessos = {}

def lfu(verboso: bool, cache_arquivos: CacheArquivos, id_arquivo: int):
    """
    Função de gerenciamento de cache LFU.
    Usa um dicionário externo 'frequencia_acessos' para controlar a contagem.
    """
    tempo_inicio = perf_counter()
    texto = verifica_cache_lfu(cache_arquivos, id_arquivo)
    if verboso:
        print(f"Conteúdo do texto:\n{texto}")
    tempo_fim = perf_counter()
    tempo_total = tempo_fim-tempo_inicio
    return tempo_total


def verifica_cache_lfu(cache_arquivos: CacheArquivos, id_arquivo: int):
    """
    Lógica principal do LFU. Se o arquivo está no cache, incrementa sua frequência.
    Se não está, o carrega. Se o cache estiver cheio, remove o de menor frequência antes de adicionar.
    """

    if cache_arquivos.contem_arquivo(id_arquivo):
        # --- CACHE HIT ---
        frequencia_acessos[id_arquivo] += 1  # Apenas incrementa a frequência
        arquivo = cache_arquivos.get_arquivo_pelo_id(
            id_arquivo)
    else:
        # --- CACHE MISS ---
        arquivo = ler_arquivo(id_arquivo)

        # Se o cache está cheio, executa a lógica de remoção LFU
        if len(cache_arquivos.ordem) >= cache_arquivos.get_max_size():
            # Encontra o item menos frequentemente usado para remover
            id_para_remover = -1
            min_freq = float('inf')

            # Itera sobre os itens NA ORDEM em que estão no cache
            # Isso serve como critério de desempate (o mais antigo entre os de menor frequência será removido)
            for id_item_cache in cache_arquivos.ordem:
                if frequencia_acessos.get(id_item_cache, 0) < min_freq:
                    min_freq = frequencia_acessos[id_item_cache]
                    id_para_remover = id_item_cache

            # Encontra o índice e remove do cache e do tracker de frequência
            idx_para_remover = cache_arquivos.ordem.index(id_para_remover)
            cache_arquivos.remover(idx_para_remover)
            del frequencia_acessos[id_para_remover]

        # Adiciona o novo arquivo ao cache e inicia sua frequência
        cache_arquivos.add_arquivo(id_arquivo, arquivo)
        frequencia_acessos[id_arquivo] = 1
    return arquivo
