# GRUPO_1_RA2

Comparativo de algoritmos de cache em um leitor de textos com simulação de desempenho.

Aluno A – Interface principal (ra2_main.py)
Função e responsabilidade

O arquivo ra2_main.py é o ponto de entrada do projeto.
Ele fornece uma interface simples no terminal que permite:

Escolher qual algoritmo de cache será usado: FIFO, LRU, LFU ou MRU;

Informar o número do texto que deseja abrir (de 1 a 100);

Executar o modo de simulação (-1), que chama os módulos da pasta simulation/;

Encerrar o programa (0).

O objetivo é facilitar os testes práticos dos algoritmos e coletar métricas de tempo de acesso, hits e requisições.

Estrutura do menu
Escolha o algoritmo:
1. FIFO
2. LRU
3. LFU
4. MRU
-1. Simulação
0. Sair


Após escolher o algoritmo, o usuário informa o número do texto a ser carregado:

Número do texto (0=voltar):


O programa verifica se o arquivo texts/<n>.txt existe.
Se não existir, mostra:

→ O arquivo texts/123.txt não existe. Tente outro número.


e solicita novamente o número, sem encerrar o programa.

Integração com os algoritmos

Conforme a opção escolhida, o ra2_main.py chama diretamente as funções:

fifo_fun(True, cache, bloco=n)
lru_fun(True,  cache, bloco=n)
mru_fun(True,  cache, bloco=n)


ou utiliza a classe LFUCache no caso do algoritmo LFU.

Cada execução exibe:

Tempo médio de resposta (ms);

Contadores de hits e requisições (requests).

Modo de simulação

Ao escolher -1, o programa importa e executa:

from simulator import run_full_simulation
run_full_simulation()


O módulo simulation/simulator.py utiliza data_collector.py e report_generator.py para:

Simular 3 usuários, cada um com 200 solicitações;

Gerar acessos conforme três distribuições:

Aleatória pura;

Poisson;

Ponderada (43 % de chance para textos 30–40);

Avaliar os algoritmos FIFO, LRU e LFU, coletando dados de hit/miss e tempo;

Salvar gráficos e relatório final na pasta docs/.

Exemplo de uso
python ra2_main.py
# Escolha 1 para FIFO
# Digite o número do texto (ex: 7)
# Saída esperada:
TEXTO
# [Tempo: 3.2 ms] | Hits: 2 | Reqs: 5

---
## Aluno B e C (Giuliano)

## Documentação: Cache e algoritmos

Nesta seção descrevemos a estrutura de dados usada como cache (algorithms/cache_arquivos.py) e os algoritmos de gerenciamento (FIFO, LRU, MRU) implementados em algorithms/fifo.py, algorithms/lru.py e algorithms/mru.py.

### Estrutura: CacheArquivos

Resumo rápido
- `ordem: list[int]` — lista que guarda os ids dos arquivos na ordem de inserção/uso (o final da lista representa o mais recente).
- `cache: dict[int, str]` — mapeia id -> conteúdo do arquivo (string).
- `max_size: int` — capacidade máxima do cache (padrão: 10).
- `hits, requests` — contadores de acertos e requisições ao cache.

Principais métodos e comportamento
- `get_arquivo_pelo_id(id_arquivo) -> str`: retorna o conteúdo salvo em `cache[id_arquivo]`.
- `contem_arquivo(id_arquivo) -> bool`: incrementa os `requests`. Retorna `True` e incrementa `hits` se o id está no cache.  
- `add_arquivo(id_arquivo, conteudo) -> bool`: tenta inserir/atualizar. Se o cache estiver cheio, não remove nada e retorna `False` (o chamador decide a política de remoção). Se houver espaço, adiciona o id ao final de `ordem` e grava em `cache` retornando `True`.
- `remover_primeiro() -> dict`: remove e retorna o item mais antigo (primeiro da `ordem`) — usado por políticas que precisam remover o mais antigo (FIFO/LRU quando necessário).
- `remover_ultimo() -> dict`: remove e retorna o item mais recente (último da `ordem`) — usado por políticas MRU.
- `remover(idx) -> dict`: remove pelo índice em `ordem`.
- `move_para_final(id_arquivo) -> None`: move um id já presente para o final da lista (marca como mais recentemente usado).
- Contadores: `inc_requests()` e `inc_hits()` atualizam `requests` e `hits` respectivamente.

### Algoritmos

Todos os algoritmos expõem a função com a mesma assinatura:

- `medir_algoritmo(verboso: bool, cache_arquivos: CacheArquivos, bloco: int) -> float`

Onde:
- `verboso=True` imprime o conteúdo do texto carregado.
- `verboso=False` não imprime nada, apenas executa.
- Retornam o tempo de execução (float) medido com `perf_counter()`.

Cada algoritmo usa uma função auxiliar `algoritmo(cache_arquivos, id_arquivo) -> str` que:
1. verifica se o id está no cache
2. se o id estiver no cache: pode atualiza `ordem` (dependendo da política) e retorna o conteúdo do arquivo lido do cache;
3. se o id não estiver no cache: lê o arquivo com `algorithms.leitor_arquivos.ler_arquivo(id)`, tenta `add_arquivo`; se `add_arquivo` retornar `False` (cache cheio), executa a remoção adequada (ver abaixo) e tenta `add_arquivo` novamente. Retorna o conteúdo do arquivo lido.

#### FIFO
- Política: First-In, First-Out — quando o cache está cheio remove o mais antigo (`remover_primeiro()`).
- Comportamento no código: ao acessar um id, se está no cache conta como hit; se não está, lê o arquivo e tenta inserir; se não couber, remove o primeiro e insere.


#### LRU
- Política: Least Recently Used — ao acessar um item que já está no cache, ele é marcado como mais recentemente usado (`move_para_final`). Quando o cache estiver cheio e for necessário inserir, o item a ser removido é o mais antigo (`remover_primeiro()`).
- Comportamento: semelhante ao FIFO para misses, mas em acessos bem-sucedidos atualiza a ordem para refletir uso recente.

#### MRU
- Política: Most Recently Used — quando o cache está cheio e precisa desalocar, remove o item mais recentemente usado (`remover_ultimo()`).
- Comportamento no código: em miss tenta `add_arquivo`; se cheio remove o último (mais recente) e insere. Em hit, o código também chama `move_para_final(id)` (o que mantém o item como mais recente) e incrementa hits.
- Observação: o comportamento no hit (chamar `move_para_final`) mantém o padrão de que o final da lista representa o mais recente; a remoção por falta de espaço remove esse último elemento.

### Exemplo de uso (em Python)
```python
from algorithms.cache_arquivos import CacheArquivos
from algorithms.lru import lru

cache = CacheArquivos()
# Executa LRU não verboso em 1 arquivo (1.txt)
tempo = lru(False, cache, 1)
print(f"Tempo: {tempo}, hits: {cache.get_hits()}, requests: {cache.get_requests()}")
```
### Métricas coletadas
- `requests`: número total de acessos a arquivos (tentativas de leitura via cache).
- `hits`: número de acessos que encontraram o arquivo no cache.
- A razão `hits/requests` indica a taxa de acerto do cache.

---
## Testes e Validação

Para garantir a corretude e o desempenho de cada algoritmo de cache, foram criados testes unitários específicos para cada política (FIFO, LRU e MRU). A metodologia de teste foi padronizada para validar dois cenários principais:

1.  **Cenário de Pior Caso (Sem Hits):** Uma sequência de acesso a arquivos projetada para nunca encontrar um valor em cache. Isso serve como linha de base de desempenho (o mais lento) e valida que o contador de hits permanece em 0.
2.  **Cenário Controlado (Com Hits):** Uma sequência de acesso cuidadosamente elaborada para gerar um número previsível de acertos (hits), testando a lógica de inserção, acerto e substituição de cada algoritmo.

Todos os testes utilizam asserções (`assert`) para verificar se o número de hits obtido é igual ao esperado e se o tempo de execução do cenário com hits é, de fato, menor que o do cenário sem hits.

### Teste FIFO (First-In, First-Out)

-   **Como foi testado:**
    -   **Sem Hits:** Foi usada uma sequência de 30 acessos a 15 arquivos distintos de forma repetida (`1, 2, ..., 15, 1, 2, ...`). Como o cache tem capacidade para 10 itens, quando o arquivo `1` é solicitado pela segunda vez, ele já foi removido para dar lugar a arquivos mais novos, garantindo 0 hits.
    -   **Com Hits:** A sequência enche o cache (`1` a `10`), depois acessa itens que ainda estão presentes (`3,5,7,9`), gerando 4 hits. Em seguida, novos itens são inseridos, forçando a remoção dos mais antigos (`1` a `6`). Acessos subsequentes a itens que estão no cache (`7,8,9,10,7,8,9,10,7,8`) geram mais 10 `hits`, totalizando 14.
-   **Resultados:** O teste passou com sucesso. O cenário "sem hits" registrou 0 hits, e o cenário "com hits" registrou exatamente 14 hits, como esperado. O tempo de execução do segundo cenário foi comprovadamente menor.

### Teste LRU (Least Recently Used)

-   **Como foi testado:**
    -   **Sem Hits:** A mesma estratégia do FIFO foi utilizada, garantindo que nenhum item fosse encontrado no cache.
    -   **Com Hits:** A sequência primeiro enche o cache (`1` a `10`). Depois, acessa `3,5,7,9`, que além de gerarem 4 hits, são movidos para o final da fila como "mais recentemente usados". Quando novos itens são inseridos, a política LRU remove os "menos recentemente usados" (`1,2,4,6,8,10`). Acessos posteriores a `3,5,7,9` resultam em mais 4 hits, pois eles foram "protegidos" pelo acesso recente. Fazendo mais 8 acessos `3,5,7,9,3,5,7,9`, totalizam 16 hits.
-   **Resultados:** O teste validou a lógica do LRU. Foram obtidos 0 hits no primeiro cenário e 16 hits no segundo. A asserção de desempenho (`tempo_sem_hits > tempo_hits`) foi confirmada.

### Teste MRU (Most Recently Used)

-   **Como foi testado:**
    -   **Sem Hits:** Foi utilizada uma sequência de 30 acessos a 30 arquivos diferentes (`1` a `30`), o que naturalmente impede qualquer acerto no cache de tamanho 10.
    -   **Com Hits:** A sequência enche o cache (`1` a `10`), depois acessa `8,9,10`, gerando 3 hits. Estes se tornam os "mais recentemente usados". A inserção de `11,12,13` força a remoção justamente dos mais recentes, como dita a política MRU (o `11` remove o `10`, o `12` remove o `11`, etc.). Acessos posteriores a `9,8` (que não foram removidos) e a `1,2,3` (que eram os mais antigos e, portanto, "protegidos" pela política) geram mais 5 hits. Após, são feitos mais 4 hits em `4,5,6,1` para totalizar os 30 acessos, somando os 12 esperados.
-   **Resultados:** A implementação do MRU foi validada com sucesso. O teste confirmou 0 hits no pior caso e 12 hits no cenário controlado, além de demonstrar a vantagem de desempenho do cache.
