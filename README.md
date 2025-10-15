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