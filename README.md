# GRUPO_1_RA2
Comparativo de algoritmos de cache em um leitor de textos com simulação de desempenho.

---

## Módulos de Análise de Performance

Para garantir que a aplicação "Texto é Vida" seja não apenas funcional, mas também altamente eficiente, foram desenvolvidos módulos específicos para a implementação e análise de performance de algoritmos de cache. O objetivo é tomar uma decisão de engenharia baseada em dados concretos sobre qual estratégia de cache adotar.

### Algoritmo de Cache LFU (Least Frequently Used)

O LFU é uma estratégia de cache que prioriza manter em memória os arquivos que são acessados com maior frequência, independentemente de quão recente foi seu último acesso.

#### Descrição e Lógica

O princípio do LFU é simples: a cada solicitação de um arquivo, sua contagem de acessos é incrementada. Quando o cache atinge sua capacidade máxima e um novo arquivo precisa ser armazenado, o algoritmo identifica e remove o arquivo que possui a menor contagem de acessos (o "menos frequentemente usado").

Nossa implementação, localizada em `algorithms/lfu.py`, atua como uma camada de lógica sobre a estrutura de dados base `CacheArquivos`.

#### Requisitos de Implementação

1.  **Rastreamento de Frequência:** O algoritmo deveria ser capaz de contar o número de vezes que cada arquivo presente no cache foi solicitado. Isso foi alcançado utilizando um dicionário auxiliar (`frequencia_acessos`) que mapeia o ID do arquivo à sua contagem de acessos.
2.  **Lógica de Evicção:** Ao atingir a capacidade máxima, o algoritmo deve identificar corretamente o arquivo com a menor frequência de acessos para remoção.
3.  **Critério de Desempate:** No cenário onde múltiplos arquivos compartilham a mesma frequência mínima, foi implementado um critério de desempate: o algoritmo remove o arquivo que foi inserido no cache há mais tempo (lógica FIFO - First-In, First-Out, entre os menos frequentes).
4.  **Integração Modular:** A função `lfu()` foi projetada para operar sobre a classe `CacheArquivos`, manipulando-a externamente sem modificar sua estrutura interna, garantindo um design de software limpo e desacoplado.

---

### Modo de Simulação Avançado

Para validar a eficácia do LFU e compará-lo com outras estratégias, foi criado um robusto modo de simulação. Este módulo, ativado com a entrada `-1`, é a principal ferramenta para a tomada de decisão sobre qual algoritmo de cache será utilizado na versão final da aplicação.

#### Descrição e Objetivos

O simulador executa um conjunto exaustivo de testes automatizados, imitando diferentes padrões de uso da aplicação por múltiplos usuários. O objetivo principal é coletar dados de performance de cada algoritmo de cache sob estresse e gerar um relatório claro e conclusivo.

#### Requisitos de Funcionalidade

1.  **Múltiplos Usuários:** A simulação deveria modelar o comportamento de **3 usuários simultâneos**, com cada um realizando **200 solicitações** de arquivos, totalizando 600 solicitações por cenário.
2.  **Padrões de Acesso Variados:** Para testar a adaptabilidade dos algoritmos, foram implementados três padrões distintos de sorteio de arquivos:
    * **Aleatório Puro:** Todas as 100 chaves de texto possuem a mesma probabilidade de serem escolhidas. Simula um comportamento de usuário totalmente imprevisível.
    * **Distribuição de Poisson:** As solicitações se concentram em torno de um "ponto de interesse" (ex: textos próximos ao ID 50), simulando um tópico ou caso que se torna temporariamente popular.
    * **Aleatório Ponderado:** Simula o cenário mais realista, onde um subconjunto de arquivos (IDs 30 a 40) é significativamente mais importante, recebendo **43% de todas as solicitações**.
3.  **Coleta de Métricas:** Para cada uma das milhares de solicitações, o sistema deveria registrar:
    * O resultado do acesso: `Cache Hit` (sucesso) ou `Cache Miss` (falha).
    * O tempo de carregamento total em segundos.
    * O algoritmo, usuário e padrão de acesso associados à solicitação.
4.  **Relatório Automatizado:** Ao final da execução, a simulação deve analisar todos os dados coletados e gerar automaticamente, na pasta `/reports`, um conjunto de artefatos:
    * **Gráficos comparativos** em formato PNG, visualizando a taxa de sucesso, tempo de resposta e distribuição de falhas.
    * **Um relatório em texto (`.txt`)** resumindo as métricas, analisando a performance e fornecendo uma recomendação final.

---

## Metodologia de Teste e Validação

Para garantir uma análise justa e precisa, a performance do algoritmo **LFU** foi testada comparativamente contra o algoritmo clássico **LRU (Least Recently Used)**.

#### Ambiente de Teste

A simulação foi projetada para ser um ambiente controlado. O acesso ao disco é simulado (através da leitura real do arquivo e uma pequena latência adicional fixa), permitindo que a diferença de tempo entre um `Cache Hit` (acesso à memória, extremamente rápido) e um `Cache Miss` (acesso ao disco, lento) seja a principal variável de performance. Cada algoritmo inicia cada cenário de teste com um cache completamente limpo.

#### Cenários de Teste

Cada algoritmo (`LFU` e `LRU`) foi submetido à bateria completa de 3.600 solicitações (3 usuários x 200 solicitações x 3 padrões de acesso x 2 algoritmos), passando por todos os cenários de acesso (Aleatório, Poisson e Ponderado).

#### Resultados Esperados

Com base na teoria de funcionamento dos algoritmos, as hipóteses para os testes eram:

1.  **No padrão Aleatório Puro:** Esperava-se uma performance baixa e similar para ambos os algoritmos, pois a falta de um padrão claro dificulta a predição.
2.  **No padrão de Poisson:** Esperava-se uma pequena vantagem para o **LFU**, por sua capacidade de identificar e manter o "hotspot" de arquivos populares no cache, mesmo que eles não sejam os mais recentes.
3.  **No padrão Ponderado:** Esperava-se uma **vitória decisiva para o LFU**. Este cenário é o ideal para o LFU, que rapidamente identificaria os textos 30-40 como altamente frequentes e os manteria no cache, resultando em uma taxa de `Cache Hit` drasticamente superior à do LRU.

O relatório final gerado pela simulação serve como a evidência empírica para confirmar ou refutar essas hipóteses, fornecendo uma base sólida para a escolha do algoritmo mais eficiente para o sistema "Texto é Vida".
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
