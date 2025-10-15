# ra2_main.py — Orquestrador do Aluno A (menu + integração dos módulos do grupo)

from algorithms.lfu_cache import lfu as lfu_fun
from algorithms.mru import medir_mru as mru_fun
from algorithms.lru import medir_lru as lru_fun
from algorithms.fifo import medir_fifo as fifo_fun
from algorithms.cache_arquivos import CacheArquivos
from simulation.simulator import run_full_simulation
from pathlib import Path

# ------------------------------------------------------------
# Paths e sys.path
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
TEXTS_DIR = BASE_DIR / "texts"

# ------------------------------------------------------------
# Utilidades locais
# ------------------------------------------------------------


def arquivo_existe(n: int) -> bool:
    return (TEXTS_DIR / f"{n}.txt").exists()


def ler_int(prompt: str) -> int:
    while True:
        s = input(prompt).strip()
        try:
            return int(s)
        except ValueError:
            print("→ Digite um número inteiro válido.")

# ------------------------------------------------------------
# Execuções por algoritmo (chamando assinaturas já existentes)
# ------------------------------------------------------------


def executar_algoritmo(nome_algoritmo: str):
    cache = CacheArquivos()
    print(
        f"\nExecutando {nome_algoritmo.upper()}. Digite 0 para voltar ao menu.\n")

    while True:
        n = ler_int("Número do texto (0=voltar): ")

        if n == 0:
            break
        if n < 1 or n > 100:
            print("→ Informe um número entre 1 e 100.")
            continue
        if not arquivo_existe(n):
            print(f"→ O arquivo texts/{n}.txt não existe. Tente outro número.")
            continue

        if nome_algoritmo == "fifo":
            dt = fifo_fun(True, cache, n)
        elif nome_algoritmo == "lru":
            dt = lru_fun(True, cache, n)
        elif nome_algoritmo == "mru":
            dt = mru_fun(True, cache, n)
        elif nome_algoritmo == "lfu":
            dt = lfu_fun(True, cache, n)
        else:
            print("Algoritmo inválido.")
            break

        dt = dt * 1000.0
        try:
            print(
                f"[Tempo: {dt:.1f} ms] | Hits: {cache.get_hits()} | Reqs: {cache.get_requests()}")
        except Exception:
            print(f"[Tempo: {dt:.1f} ms]")
        print("-" * 50)

# ------------------------------------------------------------
# Modo Simulação — chama diretamente simulation.simulator.run_full_simulation()
# ------------------------------------------------------------


def executar_simulacao():
    print("\n[MODO SIMULAÇÃO]\n")
    try:
        run_full_simulation()
    except ModuleNotFoundError as e:
        # dependências comuns da simulação
        name = str(e).split("'")[1]
        print(
            f"[simulação] Falta instalar o pacote '{name}'. Ex.: pip install {name}")
    except Exception as e:
        print(f"[simulação] Erro ao executar a simulação: {e}")

# ------------------------------------------------------------
# Menu principal
# ------------------------------------------------------------


def main():
    while True:
        print("\nEscolha o algoritmo:")
        print("1.  FIFO")
        print("2.  LRU")
        print("3.  LFU")
        print("4.  MRU")
        print("-1. Simulação")
        print("0.  Sair")

        op = ler_int("\nOpção: ")

        if op == 0:
            print("Encerrando…")
            break
        elif op == -1:
            executar_simulacao()
        elif op == 1:
            executar_algoritmo("fifo")
        elif op == 2:
            executar_algoritmo("lru")
        elif op == 3:
            executar_algoritmo("lfu")
        elif op == 4:
            executar_algoritmo("mru")
        else:
            print("→ Opção inválida. Tente novamente.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
