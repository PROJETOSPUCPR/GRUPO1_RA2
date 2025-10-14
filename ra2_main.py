# ra2_main.py — Orquestrador do Aluno A (menu + integração dos módulos do grupo)

import time
from pathlib import Path
import sys
import importlib

# ------------------------------------------------------------
# Paths e sys.path
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
TEXTS_DIR = BASE_DIR / "texts"

# Coloca a RAIZ no sys.path (para 'algorithms.*' e 'simulation.*')
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# ------------------------------------------------------------
# Imports dos colegas (sem alterar código deles)
# ------------------------------------------------------------
from algorithms.cache_arquivos import CacheArquivos
from algorithms.fifo import fifo as fifo_fun
from algorithms.lru import lru as lru_fun
from algorithms.mru import mru as mru_fun

# LFU pode estar como classe LFUCache OU função lfu(...)
LFU_IS_CLASS = False
try:
    from algorithms.lfu_cache import LFUCache  # classe
    LFU_IS_CLASS = True
except Exception:
    from algorithms.lfu_cache import lfu as lfu_fun  # função

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
def executar_fifo_lru_mru(nome_algoritmo: str):
    cache = CacheArquivos()
    print(f"\nExecutando {nome_algoritmo.upper()}. Digite 0 para voltar ao menu.\n")

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

        t0 = time.perf_counter()

        if nome_algoritmo == "fifo":
            fifo_fun(True, cache, bloco=n)
        elif nome_algoritmo == "lru":
            lru_fun(True, cache, bloco=n)
        elif nome_algoritmo == "mru":
            mru_fun(True, cache, bloco=n)
        else:
            print("Algoritmo inválido."); break

        dt = (time.perf_counter() - t0) * 1000.0
        try:
            print(f"[Tempo: {dt:.1f} ms] | Hits: {cache.get_hits()} | Reqs: {cache.get_requests()}")
        except Exception:
            print(f"[Tempo: {dt:.1f} ms]")
        print("-" * 50)

def executar_lfu():
    print("\nExecutando LFU. Digite 0 para voltar ao menu.\n")

    # Se for classe, instanciamos; se for função, usamos CacheArquivos como nos demais
    cache = CacheArquivos()
    lfu_instance = None
    if LFU_IS_CLASS:
        try:
            lfu_instance = LFUCache()  # muitas versões já configuram internamente max_size=10
        except TypeError:
            lfu_instance = LFUCache  # fallback extremamente raro

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

        t0 = time.perf_counter()

        if LFU_IS_CLASS and callable(getattr(lfu_instance, "get", None)):
            # contrato típico de classe LFUCache com get/put
            texto = lfu_instance.get(n)
            if texto is None:
                # miss → carrega do disco e armazena
                texto = (TEXTS_DIR / f"{n}.txt").read_text(encoding="utf-8")
                if hasattr(lfu_instance, "put"):
                    lfu_instance.put(n, texto)
        else:
            # fallback: função lfu(dinamico=True, cache_arquivos=..., bloco=n)
            lfu_fun(True, cache, bloco=n)

        dt = (time.perf_counter() - t0) * 1000.0
        try:
            print(f"[Tempo: {dt:.1f} ms] | Hits: {cache.get_hits()} | Reqs: {cache.get_requests()}")
        except Exception:
            print(f"[Tempo: {dt:.1f} ms]")
        print("-" * 50)

# ------------------------------------------------------------
# Modo Simulação — chama diretamente simulation.simulator.run_full_simulation()
# ------------------------------------------------------------
def executar_simulacao():
    print("\n[MODO SIMULAÇÃO]\n")
    try:
        import importlib, sys

        # --- 1) SHIM p/ LFUCache (simulação espera classe; você tem função lfu(...)) ---
        lfu_mod = importlib.import_module("algorithms.lfu_cache")
        if not hasattr(lfu_mod, "LFUCache"):
            lfu_func = getattr(lfu_mod, "lfu", None)
            if lfu_func is None or not callable(lfu_func):
                raise ImportError("algorithms.lfu_cache não possui LFUCache nem a função lfu(...).")

            class LFUCache:
                def __init__(self, *args, **kwargs):
                    pass
                def __call__(self, *args, **kwargs):
                    # permitir LFUCache()(dinamico=True, cache, bloco=...)
                    return lfu_func(*args, **kwargs)

            setattr(lfu_mod, "LFUCache", LFUCache)
            sys.modules["algorithms.lfu_cache"] = lfu_mod

        # --- 2) SHIMS p/ lru/fifo/mru como "fábricas" sem argumentos ---
        # O simulator faz: algorithms = {'LRU': lru(), 'FIFO': fifo(), 'MRU': mru(), 'LFU': LFUCache()}
        # Então precisamos que lru()/fifo()/mru() retornem a função original chamável.
        for modname, fname in [
            ("algorithms.lru", "lru"),
            ("algorithms.fifo", "fifo"),
            ("algorithms.mru", "mru"),
        ]:
            mod = importlib.import_module(modname)
            orig = getattr(mod, fname, None)
            if callable(orig):
                # se já é fábrica (aceita zero args), mantém; senão, cria wrapper
                try:
                    # tentativa de chamada sem args — se der TypeError, precisamos do wrapper
                    import inspect
                    sig = inspect.signature(orig)
                    if len(sig.parameters) == 0:
                        # já é fábrica, segue o jogo
                        pass
                    else:
                        # fábrica: sem args → retorna a função original
                        def make_factory(func):
                            def factory():
                                return func
                            return factory
                        setattr(mod, fname, make_factory(orig))
                        sys.modules[modname] = mod
                except Exception:
                    # por segurança, aplica wrapper
                    def make_factory(func):
                        def factory():
                            return func
                        return factory
                    setattr(mod, fname, make_factory(orig))
                    sys.modules[modname] = mod

        # --- 3) Limpa caches e importa o simulador só agora (com os shims no lugar) ---
        importlib.invalidate_caches()
        sim_mod = importlib.import_module("simulation.simulator")

        # --- 4) Executa ---
        if hasattr(sim_mod, "run_full_simulation") and callable(sim_mod.run_full_simulation):
            sim_mod.run_full_simulation()
        else:
            raise AttributeError("simulation.simulator não expõe run_full_simulation().")

    except ModuleNotFoundError as e:
        # dependências comuns da simulação
        name = str(e).split("'")[1]
        print(f"[simulação] Falta instalar o pacote '{name}'. Ex.: pip install {name}")
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
            print("Encerrando…"); break
        elif op == -1:
            executar_simulacao()
        elif op == 1:
            executar_fifo_lru_mru("fifo")
        elif op == 2:
            executar_fifo_lru_mru("lru")
        elif op == 3:
            executar_lfu()
        elif op == 4:
            executar_fifo_lru_mru("mru")
        else:
            print("→ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
