# /algorithms/lfu.py

from algorithms.leitor_arquivos import ler_arquivo
from algorithms.cache_arquivos import CacheArquivos

# Dicionário para rastrear a frequência de cada arquivo no cache.
# Ele será passado junto com o cache para a função.
frequencia_acessos = {}

def lfu(dinamico: bool, cache_arquivos: CacheArquivos, blocos: list[int] | None = None, bloco: int | None = None):
    """
    Função de gerenciamento de cache LFU.
    Usa um dicionário externo 'frequencia_acessos' para controlar a contagem.
    """
    if dinamico and bloco is not None:
        verifica_cache_lfu(cache_arquivos, bloco)
    elif blocos:
        for item in blocos:
            verifica_cache_lfu(cache_arquivos, item)
    else:
        raise ValueError("Argumentos inválidos/faltando para a função LFU.")

def verifica_cache_lfu(cache_arquivos: CacheArquivos, id_arquivo: int):
    """
    Lógica principal do LFU. Se o arquivo está no cache, incrementa sua frequência.
    Se não está, o carrega. Se o cache estiver cheio, remove o de menor frequência antes de adicionar.
    """
    cache_arquivos.inc_requests()
    
    if cache_arquivos.contem_arquivo(id_arquivo):
        # --- CACHE HIT ---
        cache_arquivos.inc_hits()
        frequencia_acessos[id_arquivo] += 1 # Apenas incrementa a frequência
    else:
        # --- CACHE MISS ---
        conteudo = ler_arquivo(id_arquivo)
        
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
        cache_arquivos.add_arquivo(id_arquivo, conteudo)
        frequencia_acessos[id_arquivo] = 1