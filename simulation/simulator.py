
# /simulation/simulator.py
# /simulation/simulator.py

import time
import numpy as np

# A importação dos algoritmos continua a mesma
from algorithms.cache_arquivos import CacheArquivos
from algorithms.lfu_cache import LFUCache
from algorithms.lru import lru
from algorithms.fifo import fifo 
from algorithms.mru import mru
from algorithms.leitor_arquivos import ler_arquivo
from simulation.data_collector import DataCollector
from simulation.report_generator import generate_report

# --- As funções de geração de padrões (generate_pure_random, etc.) permanecem inalteradas ---
def generate_pure_random(n_requests, n_texts):
    return np.random.randint(1, n_texts + 1, size=n_requests)

def generate_poisson(n_requests, n_texts, lambda_val=50):
    requests = np.random.poisson(lambda_val, size=n_requests)
    return np.clip(requests, 1, n_texts)

def generate_weighted(n_requests, n_texts):
    texts = np.arange(1, n_texts + 1)
    prob_focused = 0.43 / 11
    prob_other = (1 - 0.43) / (n_texts - 11)
    probabilities = np.full(n_texts, prob_other)
    probabilities[29:40] = prob_focused
    return np.random.choice(texts, size=n_requests, p=probabilities)

# --- Lógica Principal da Simulação ---

def run_full_simulation():
    """
    Orquestra a simulação completa. A única mudança é na inicialização dos algoritmos.
    """
    print("\n" + "="*15 + " INICIANDO MODO DE SIMULAÇÃO " + "="*15)
    
    # Configurações da Simulação
    N_USERS = 3
    N_REQUESTS_PER_USER = 200
    N_TEXTS = 100
    # O tamanho do cache agora é definido internamente pela classe CacheArquivos (max_size=10)
    DISK_LATENCY = 0.01

    # Componentes da Simulação
    collector = DataCollector()
    
    # **MUDANÇA AQUI**: Os construtores não precisam mais do argumento 'capacity'.
    algorithms = {
        'LFU': LFUCache(),
        'LRU': lru(),
        'FIFO': fifo(),
        'MRU': mru()
    }
    
    patterns = {
        'Aleatório Puro': generate_pure_random,
        'Distribuição de Poisson': generate_poisson,
        'Ponderado (Foco 30-40)': generate_weighted
    }
    
    total_sims = len(algorithms) * len(patterns)
    current_sim = 0

    for algo_name, algo_func in algorithms.items():
        for pattern_name, generator_func in patterns.items():
            current_sim += 1
            print(f"\nExecutando Simulação [{current_sim}/{total_sims}]: Algoritmo='{algo_name}', Padrão='{pattern_name}'...")
            
            # Cria uma instância de cache limpa para este teste
            cache = CacheArquivos()

            for user_id in range(1, N_USERS + 1):
                requests = generator_func(N_REQUESTS_PER_USER, N_TEXTS)
                
                for text_id in requests:
                    # Precisamos verificar o status do hit ANTES da chamada
                    hits_before = cache.get_hits()
                    
                    start_time = time.perf_counter()
                    
                    # Chama a função do algoritmo no modo dinâmico (um bloco por vez)
                    algo_func(dinamico=True, cache_arquivos=cache, bloco=text_id)
                    time.sleep(DISK_LATENCY) # Adiciona a latência simulada
                    
                    end_time = time.perf_counter()
                    time_taken = end_time - start_time
                    
                    # Compara os hits para determinar se foi um sucesso
                    hits_after = cache.get_hits()
                    is_hit = hits_after > hits_before
                    
                    collector.record(user_id, algo_name, pattern_name, text_id, is_hit, time_taken)

    results_df = collector.get_dataframe()
    generate_report(results_df)
    
    print("\n" + "="*17 + " SIMULAÇÃO CONCLUÍDA " + "="*17)
    print("Pressione Enter para retornar ao menu principal...")
    input()