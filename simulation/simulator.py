
# /simulation/simulator.py

import time
import numpy as np

from algorithms.lfu_cache import LFUCache
from algorithms.lru_cache import LRUCache
from simulation.data_collector import DataCollector
from simulation.report_generator import generate_report

# --- Funções para Geração de Padrões de Solicitação ---

def generate_pure_random(n_requests, n_texts):
    """Gera uma sequência de solicitações puramente aleatórias."""
    return np.random.randint(1, n_texts + 1, size=n_requests)

def generate_poisson(n_requests, n_texts, lambda_val=50):
    """Gera solicitações com distribuição de Poisson, centrada em lambda_val."""
    requests = np.random.poisson(lambda_val, size=n_requests)
    # Garante que os valores estejam no intervalo [1, n_texts]
    return np.clip(requests, 1, n_texts)

def generate_weighted(n_requests, n_texts):
    """Gera solicitações com peso: 43% de chance para textos 30-40."""
    texts = np.arange(1, n_texts + 1)
    
    # Calcula a probabilidade para cada texto
    prob_focused = 0.43 / 11  # 43% dividido entre 11 textos (30 a 40)
    prob_other = (1 - 0.43) / (n_texts - 11)
    
    probabilities = np.full(n_texts, prob_other)
    probabilities[29:40] = prob_focused # Índices 29 a 39 correspondem aos textos 30 a 40
    
    return np.random.choice(texts, size=n_requests, p=probabilities)

# --- Lógica Principal da Simulação ---

def run_full_simulation():
    """
    Orquestra a simulação completa, testando todos os algoritmos
    com todos os padrões de solicitação e gerando o relatório final.
    """
    print("\n" + "="*15 + " INICIANDO MODO DE SIMULAÇÃO " + "="*15)
    
    # Configurações da Simulação
    N_USERS = 3
    N_REQUESTS_PER_USER = 200
    N_TEXTS = 100
    CACHE_SIZE = 10
    DISK_READ_TIME = 0.05 # Simula um disco mais rápido para não demorar muito

    # Componentes da Simulação
    collector = DataCollector()
    algorithms = {
        'LFU': LFUCache(capacity=CACHE_SIZE),
        'LRU': LRUCache(capacity=CACHE_SIZE)
    }
    patterns = {
        'Aleatório Puro': generate_pure_random,
        'Distribuição de Poisson': generate_poisson,
        'Ponderado (Foco 30-40)': generate_weighted
    }
    
    total_sims = len(algorithms) * len(patterns)
    current_sim = 0

    # Loop principal da simulação
    for algo_name, cache_instance in algorithms.items():
        for pattern_name, generator_func in patterns.items():
            current_sim += 1
            print(f"\nExecutando Simulação [{current_sim}/{total_sims}]: Algoritmo='{algo_name}', Padrão='{pattern_name}'...")
            
            cache_instance.clear() # Garante que o cache esteja limpo para cada teste

            for user_id in range(1, N_USERS + 1):
                requests = generator_func(N_REQUESTS_PER_USER, N_TEXTS)
                
                for text_id in requests:
                    start_time = time.perf_counter()
                    
                    content = cache_instance.get(text_id)
                    is_hit = content is not None
                    
                    if not is_hit: # Cache Miss
                        time.sleep(DISK_READ_TIME) # Simula o tempo de leitura do disco
                        # Em uma simulação, não precisamos do conteúdo real
                        cache_instance.put(text_id, "dummy_content")

                    end_time = time.perf_counter()
                    time_taken = end_time - start_time
                    
                    collector.record(user_id, algo_name, pattern_name, text_id, is_hit, time_taken)

    # Geração do Relatório Final
    results_df = collector.get_dataframe()
    generate_report(results_df)
    
    print("\n" + "="*17 + " SIMULAÇÃO CONCLUÍDA " + "="*17)
    print("Pressione Enter para retornar ao menu principal...")
    input()