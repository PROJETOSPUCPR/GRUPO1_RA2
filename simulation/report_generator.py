import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def generate_report(df: pd.DataFrame, output_dir="docs"):
    """
    Gera um relatório completo com gráficos e um sumário em texto.
    """
    if df.empty:
        print("Nenhum dado coletado para gerar o relatório.")
        return

    print("Gerando relatório de performance...")
    os.makedirs(output_dir, exist_ok=True)
    
    # Configurações de estilo para os gráficos
    sns.set_theme(style="whitegrid")

    # --- GRÁFICO 1: Cache Hits vs. Misses por Algoritmo ---
    plt.figure(figsize=(12, 7))
    hit_miss_data = df.groupby(['algorithm', 'is_hit']).size().unstack(fill_value=0)
    hit_miss_data.plot(kind='bar', stacked=True, colormap='viridis', rot=0)
    plt.title('Total de Cache Hits vs. Misses por Algoritmo', fontsize=16)
    plt.ylabel('Número de Solicitações', fontsize=12)
    plt.xlabel('Algoritmo de Cache', fontsize=12)
    plt.legend(['Miss (Falha)', 'Hit (Sucesso)'])
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '1_hits_vs_misses.png'))
    plt.close()

    # --- GRÁFICO 2: Tempo Médio de Resposta por Algoritmo e Tipo de Acesso ---
    plt.figure(figsize=(12, 7))
    sns.barplot(data=df, x='algorithm', y='time_taken', hue='is_hit', palette='coolwarm')
    plt.title('Tempo Médio de Carregamento (Hit vs. Miss)', fontsize=16)
    plt.ylabel('Tempo Médio (segundos)', fontsize=12)
    plt.xlabel('Algoritmo de Cache', fontsize=12)
    plt.legend(title='Tipo de Acesso', labels=['Miss', 'Hit'])
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '2_tempo_medio_resposta.png'))
    plt.close()

    # --- GRÁFICO 3: Distribuição de Misses por Texto ---
    misses_df = df[~df['is_hit']]
    for algo in df['algorithm'].unique():
        plt.figure(figsize=(20, 7))
        algo_misses = misses_df[misses_df['algorithm'] == algo]
        sns.histplot(data=algo_misses, x='text_id', bins=100, kde=False)
        plt.title(f'Distribuição de Cache Misses por Texto - Algoritmo {algo}', fontsize=16)
        plt.xlabel('ID do Texto', fontsize=12)
        plt.ylabel('Contagem de Misses', fontsize=12)
        plt.xlim(1, 100)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'3_misses_por_texto_{algo}.png'))
        plt.close()

    # --- RELATÓRIO EM TEXTO ---
    with open(os.path.join(output_dir, 'relatorio_final.txt'), 'w') as f:
        f.write("="*50 + "\n")
        f.write("RELATORIO DE PERFORMANCE DOS ALGORITMOS DE CACHE\n")
        f.write("="*50 + "\n\n")
        
        total_requests = len(df)
        f.write(f"Simulacao concluida com um total de {total_requests} solicitacoes.\n\n")

        for algo in df['algorithm'].unique():
            f.write(f"--- Analise do Algoritmo: {algo} ---\n")
            algo_df = df[df['algorithm'] == algo]
            total_hits = algo_df['is_hit'].sum()
            total_misses = len(algo_df) - total_hits
            hit_rate = (total_hits / len(algo_df)) * 100
            avg_time = algo_df['time_taken'].mean()
            
            f.write(f"  - Total de Hits: {total_hits}\n")
            f.write(f"  - Total de Misses: {total_misses}\n")
            f.write(f"  - Taxa de Sucesso (Hit Rate): {hit_rate:.2f}%\n")
            f.write(f"  - Tempo Medio de Resposta: {avg_time:.6f} segundos\n\n")

        # Análise do padrão Ponderado
        weighted_df = df[df['pattern'] == 'Ponderado (Foco 30-40)']
        f.write("\n--- Analise Especifica do Padrao Ponderado ---\n")
        for algo in weighted_df['algorithm'].unique():
            algo_weighted_df = weighted_df[weighted_df['algorithm'] == algo]
            hit_rate_weighted = (algo_weighted_df['is_hit'].sum() / len(algo_weighted_df)) * 100
            f.write(f"  - Taxa de Sucesso para {algo}: {hit_rate_weighted:.2f}%\n")
        
        f.write("\n--- Conclusao ---\n")
        summary = df.groupby('algorithm')['is_hit'].mean().sort_values(ascending=False)
        best_algo = summary.index[0]
        f.write(f"O algoritmo com a maior taxa de sucesso geral foi o '{best_algo}' com {summary.iloc[0]*100:.2f}%.\n")
        f.write("Recomenda-se a utilizacao deste algoritmo para a aplicacao final.\n")

    print(f"Relatorio e graficos salvos no diretorio '{output_dir}'.")
